"""Source regression tests. Pine runtime tests live in smart_trade_contract.pine."""
import importlib.util
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT / 'tools/build_smart_trade.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class SourceContract(unittest.TestCase):
    def test_generated_files_match(self):
        for path, source in build.build().items():
            self.assertEqual(path.read_text(), source, path.name)

    def test_legacy_code_preserved(self):
        baseline = subprocess.check_output(['git', 'show', '8bea838:indicator-based-version1.pine'], cwd=ROOT, text=True)
        current = (ROOT / 'indicator-based-version1.pine').read_text()
        current = re.sub(r'// BEGIN SMART TRADE .*?// END SMART TRADE [A-Z]+', '', current, flags=re.S)
        additions = [
            '// SMART TRADE HOOK: retain true wick invalidation before visual sizing.',
            '_st_raw_top = _top', '_st_raw_bottom = _bot',
            '// Snapshot at detection time, independent of legacy touched-zone removal.',
            "st_register(_zone_type == 'D' ? 1 : -1, s1_time, _top, _bot, _st_raw_top, _st_raw_bottom)",
        ]
        lines = [line for line in current.splitlines() if line.strip() and line.strip() not in additions]
        self.assertEqual(lines, [line for line in baseline.splitlines() if line.strip()])

    def test_canonical_engine_is_identical(self):
        main = (ROOT / 'indicator-based-version1.pine').read_text()
        strategy = (ROOT / 'indicator-based-version1-backtest.pine').read_text()
        for name in ['TYPES', 'ENGINE']:
            pattern = rf'// BEGIN SMART TRADE {name}.*?// END SMART TRADE {name}'
            self.assertEqual(re.search(pattern, main, re.S).group(), re.search(pattern, strategy, re.S).group())

    def test_closed_htf_and_no_intrabar_persistence(self):
        engine = (ROOT / 'modules/smart_trade_engine.pine').read_text()
        self.assertIn('bias[1]', engine)
        self.assertEqual(engine.count('[high[1], low[1], time[1]]'), 3)
        self.assertNotIn('varip ', engine)
        self.assertIn('idx > z.touched', engine)
        self.assertIn('itop_y[1]', engine)

    def test_registry_capacity_and_period_lifetime(self):
        engine = (ROOT / 'modules/smart_trade_engine.pine').read_text()
        self.assertIn('not isPeriod and bar_index - level.born > st_expiry', engine)
        self.assertIn("reason := 'Registry capacity: fail closed'", engine)
        self.assertIn('zone.side == -side and zone.valid', engine)

    def test_fixture_reuses_production_functions(self):
        fixture = (ROOT / 'tests/smart_trade_contract.pine').read_text()
        engine = (ROOT / 'modules/smart_trade_engine.pine').read_text()
        for name in ['st_target_pair', 'st_plan', 'st_prepare_trade_bar', 'st_trade_risk', 'st_cost_r', 'st_process_point', 'st_step_zone', 'st_zone_confirmable']:
            self.assertIn(build.function_block(engine, name), fixture)
        self.assertEqual(fixture.count('    st_assert('), 64)

    def test_native_entry_fill_guard(self):
        adapter = (ROOT / 'modules/smart_trade_execution.pine').read_text()
        for state in ['opentrades', 'closedtrades']:
            self.assertIn(f'strategy.{state}.entry_price(', adapter)
            self.assertIn(f'strategy.{state}.entry_bar_index(', adapter)
        self.assertIn('runtime.error(', adapter)
        self.assertIn('st_native_expected_entry := close', adapter)
        self.assertIn("st_stop_mode == 'Close full at TP1'", adapter)
        self.assertIn("qty=st_signal_qty, limit=st_signal_t1", adapter)
        self.assertIn("st_stop_mode == 'Breakeven after TP1 (next bar)'", adapter)
        self.assertIn("limit=st_trade.tp2, stop=st_trade.entry", adapter)
        self.assertNotIn(' - st_trade.entry', adapter)

    def test_baseline_rejects_unknown_htf(self):
        engine = (ROOT / 'modules/smart_trade_engine.pine').read_text()
        self.assertIn('if na(st_htf_bias) or st_htf_bias != side', engine)


if __name__ == '__main__':
    unittest.main()
