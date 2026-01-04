class StrUtils:
    @classmethod
    def split_camel_case(cls, txt: str) -> str:
        result = ""
        for i, s in enumerate(txt):
            if i > 0 and s.isupper():
                result += " " + s
                continue
            result += s

        return result
