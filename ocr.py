import pytesseract


def ldistance(a: str, b: str) -> int:
    '''levenshtein distance for two strings, ignoring case; wagner-fischer algorithm'''
    a = a.lower()
    b = b.lower()
    m, n = len(a), len(b)
    d = [[0]*(n+1)for i in range(m+1)]
    for i in range(1, m+1):
        d[i][0] = i
    for i in range(1, n+1):
        d[0][i] = i

    for j in range(1, n+1):
        for i in range(1, m+1):
            subcost = a[i-1] != b[j-1] and 1 or 0
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+subcost)
    return d[-1][-1]


class OCRData:
    def __init__(self, raw: str):
        self.raw = raw
        rawlines = raw.strip().split('\n')
        keys = rawlines[0].split('\t')
        self.rows = [{k: v for (k, v) in zip(keys, row.split('\t'))}
                     for row in rawlines[1:]]
        self.fulltext = [r['text'] for r in self.rows]

    def from_image(img, config=''):
        '''wrapper for pytesseract.image_to_data for cleanliness'''
        return OCRData(pytesseract.image_to_data(img, config=config))

    def bbox(self, index: int) -> tuple[int]:
        '''return the bounding box of the word in rows[index] as an (x,y,w,h) tuple'''
        return (int(self.rows[index][key])for key in ['left', 'top', 'width', 'height'])

    def fuzzysearch(self, key: list[str], threshold=0) -> list[int]:
        '''returns the first index of each occurrence of the given key phrase,
        where each word in the text must match the corresponding word in the key within the given threshold
        (naive version that runs in O(m*n))'''
        results = []
        for i in range(len(self.fulltext)-len(key)):
            test = [ldistance(self.fulltext[i+j], w) <= threshold for j,
                    w in enumerate(key)]
            if all(test):
                results.append(i)
        return results
