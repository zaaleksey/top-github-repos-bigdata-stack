from mrjob.job import MRJob


class MRLocation(MRJob):
    FILES = ["utils.py"]

    def mapper(self, _, line):
        # line: "155.209.225.181"	2
        from utils import get_location_by_ip
        ip, count = line.split("\t")
        location = get_location_by_ip(ip.replace('"', ''))
        yield location, int(count)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == "__main__":
    MRLocation.run()
