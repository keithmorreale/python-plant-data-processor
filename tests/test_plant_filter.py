import unittest
import tempfile
from pathlib import Path
from plant_filter import classify, run

class PlantFilterTests(unittest.TestCase):
    def test_qualified(self):
        self.assertEqual(classify({'plant_name':'A','growth_rate_cm_year':'30','mature_height_m':'5','sunlight':'full sun'},20,10,{'full sun'})[0], 'QUALIFIED')
    def test_excluded(self):
        self.assertEqual(classify({'plant_name':'A','growth_rate_cm_year':'3','mature_height_m':'5','sunlight':'full sun'},20,10,{'full sun'})[0], 'EXCLUDED')
    def test_missing_data(self):
        self.assertEqual(classify({'plant_name':'A','growth_rate_cm_year':'','mature_height_m':'5','sunlight':'full sun'},20,10,{'full sun'})[0], 'REVIEW')
    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root/'plants.csv'
            p.write_text('plant_name,growth_rate_cm_year,mature_height_m,sunlight\nA,30,5,full sun\nB,,5,shade\n')
            result = run(p, root/'results.csv', root/'summary.json', 20, 10, 'full sun')
            self.assertEqual(result['counts'],{'QUALIFIED':1,'EXCLUDED':0,'REVIEW':1})
            self.assertTrue((root/'summary.json').exists())

if __name__ == '__main__': unittest.main()
