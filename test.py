import glossary
import unittest
import tempfile

class TestGlossary(unittest.TestCase):
    def test_extract_words(self):
        content_str = """   aaa (bbb, ccc) [ddd_eee] __DDD__
                            AA+BB-CC*D/E=45
                            ttt~!@#$%^&*+-=/TTT
                            sss.,;"'SSS # comment
                            qqq{rrr} uuu vvv87www"""
        
        expected_words = {	"aaa", "bbb", "ccc", "ddd", "eee", "DDD",
                            "AA", "BB", "CC", "D", "E",
                            "ttt", "TTT", "sss", "SSS", "qqq", "rrr", "uuu", "vvv", "www", "comment"}

        words = glossary.extract_words(content_str)
        self.assertEqual(words, expected_words) # the order is not rellevant for a set()
    
    def test_glossary_add(self):
        glossary_path = None
        g = glossary.Glossary(glossary_path, load=False)
        g.add(new_words = {"aaa","bbb","ccc", "aaa"})
        self.assertEqual(g.glossary, {"ccc","bbb", "aaa"})
        g.add(new_words = {"bbb","ddd"})
        self.assertEqual(g.glossary, {"ccc","bbb","ddd", "aaa"})
    
    def test_dynamic_flow(self):
        glossary_path = None
        g = glossary.Glossary(glossary_path, load=False)
        
        content_str1 = "aaa (bbb + ccc = ddd187)"
        words1 = glossary.extract_words(content_str1)
        g.add(words1)
        
        content_str2 = "AAA [BBB + CCC = 187DDD eee_fff]"
        words2 = glossary.extract_words(content_str2)
        g.add(words2)

        expected_words = {"aaa","bbb","AAA", "ccc","BBB", "ddd", "CCC", "DDD", "eee", "fff"}
        self.assertEqual(g.glossary, expected_words)

    
if __name__ == "__main__":
    unittest.main()



