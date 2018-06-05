import arrow


class TimeConverter:
    @staticmethod
    def timestamp_to_md_format(timestamp):
        t = arrow.get(timestamp)
        try:
            t = t.to('Asia/Shanghai')
        except:
            t = arrow.utcnow().to('Asia/Shanghai')
        finally:
            return t.format("YYYY-MM-DD HH:mm:ss")
