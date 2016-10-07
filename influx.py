import influxdb

from datetime import datetime

DB = 'crazyhouse'


def readfiles():
    datas = []
    with file('result-2016-10-03.txt', 'r') as inputfile:
        for line in inputfile.readlines():
            datas.append(line.split())

    return datas


def make_measurement(datas):
    """
    :datas: A List, first item is time, second is new_house, third is second_house.
    """
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
    dbname = DB

    db = influxdb.InfluxDBClient(host, port, user, password, dbname)
    db.create_database(dbname)
    return db


def get_latest_time():
    db = get_influxdb()
    result = db.query('select * from new_house order by time desc limit 1',
                      database=DB)
    time_str = result['new_house'].next()['time']
    return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')


def insert(date, newnum, oldnum):
    db = get_influxdb()
    dts = make_measurement([[date, newnum, oldnum]])
    assert db.write_points(dts, database=DB, batch_size=50)


def main():
    print get_latest_time()


if __name__ == '__main__':
    main()
