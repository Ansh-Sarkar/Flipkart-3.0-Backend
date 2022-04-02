from contextlib import suppress
class trialContextManager:
    def __enter__(self): pass
    def __exit__(self, *args): return True
trial = trialContextManager()
a = {'message':'hello'}
b = ['yes','no']
# with trial: val = a['haha']
with suppress(BaseException): b['wer'] = a['haha']
print(b)