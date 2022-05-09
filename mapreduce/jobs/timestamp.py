from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol


class MRTimeLocation(MRJob):
    FILES = ["utils.py"]
    OUTPUT_PROTOCOL = JSONValueProtocol

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_id_with_hour,
                combiner=self.reducer,
                reducer=self.reducer
            ),
            MRStep(
                mapper=self.mapper_location_with_hour,
                combiner=self.reducer,
                reducer=self.reducer
            ),
            MRStep(
                mapper=self.mapper_for_hour,
                reducer=self.reducer_for_hour
            ),
            MRStep(
                mapper=self.mapper_data,
                reducer=self.reducer_data
            )
        ]

    def mapper_id_with_hour(self, _, line):
        # line: [2021-11-22 08:57:08.916514] 202.6.195.211
        data = line.split()
        ip = data[-1]
        hour = data[1][:2]
        if 8 <= int(hour) <= 18:
            yield (ip, hour), 1

    def mapper_location_with_hour(self, pair_ip_hour, count):
        from utils import get_location_by_ip
        ip, hour = pair_ip_hour
        location = get_location_by_ip(ip)
        yield (location, hour), count

    def reducer(self, key, values):
        yield key, sum(values)

    def mapper_for_hour(self, pair_location_hour, count):
        location, hour = pair_location_hour
        yield hour, {location: count}

    def reducer_for_hour(self, hour, data):
        yield hour, list(data)

    def mapper_data(self, hour, data):
        time = f"{hour}:00-{int(hour) + 1}:00"
        yield None, (time, data)

    def reducer_data(self, _, hour_data):
        yield None, dict(hour_data)


if __name__ == "__main__":
    MRTimeLocation.run()
