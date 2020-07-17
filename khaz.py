
class khaz:
    def __init__(self, totall, name="") -> None:
        self.name = name
        self.total = totall
        self.current = totall
        self.allTrans = []

    def khaz(self):
        total = self.total
        current = self.current
        return f'total - {total} | current - {current}'

    def makeTrans(self, usedamnt, usedFor=''):
        self.allTrans.append({'usedamnt': usedamnt, 'usedfor': usedFor})
        self.current = self.current - usedamnt
        return 'transaction successfull'

    def availkhaz(self):
        return self.current

    def showTrans(self):
        if self.allTrans == 0:
            return "no transactions yet"
        else:
            return self.allTrans