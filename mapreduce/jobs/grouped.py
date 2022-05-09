from mrjob.job import MRJob


class MRGrouped(MRJob):
    def mapper(self, _, line):
        yield line.split()[-1], 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        count = sum(values)
        if count > 1:
            yield key, count


if __name__ == "__main__":
    MRGrouped.run()
