import influxdb


def readfiles():
    datas = []
    with file('result-2016-10-03.txt', 'r') as inputfile:
        for line in inputfile.readlines():
            datas.append(line.split())

    return datas


def make_measurement(datas):
    datapoints = []

    for data in datas:
        datapoint = {
            "time": data[0],
            "measurement": "new_house",
            "fields": {
                "value": int(data[1]),
            },

        }
        datapoints.append(datapoint)

        datapoint = {
            "time": data[0],
            "measurement": "second_house",
            "fields": {
                "value": int(data[2]),
            },
        }
        datapoints.append(datapoint)

    return datapoints


def get_influxdb():
    host = 'localhost'
    port = 8086
    user = 'root'
    password = 'root'
    dbname = 'crazyhouse'

    db = influxdb.InfluxDBClient(host, port, user, password, dbname)
    db.create_database(dbname)
    return db


def main():
    datas = readfiles()
    db = get_influxdb()
    dts = make_measurement(datas)
    assert db.write_points(dts, database='crazyhouse', batch_size=50)


if __name__ == '__main__':
    main()
