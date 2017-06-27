import sqlite3


class SensorData:
    def __init__(self, dbfile):
        self._conn = sqlite3.connect(dbfile)

    def add(self, light_infrared, light_visible, light_lux,
            pressure, temperature, humidity, soil_moisture,
            light_switch_state):
        self._execute(
            '''INSERT INTO sensor_data
                  (light_infrared, light_visible, light_lux,
                   pressure, temperature, humidity, soil_moisture,
                   light_switch_state)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (light_infrared, light_visible, light_lux,
             pressure, temperature, humidity, soil_moisture,
             light_switch_state)
        )
        self._conn.commit()

    def get_current_avg_lux(self, timeframe_minutes):
        result = self._execute(
            ('''SELECT AVG(light_lux)
               FROM sensor_data
               WHERE
                recorded_at >= DATETIME('NOW', '-%d Minute')''' %
             int(timeframe_minutes)),
            []
        ).fetchone()
        return result[0]

    def get_aggregated_values(self, timeframe_minutes):
        result = self._execute(
            ('''SELECT
                    CURRENT_TIMESTAMP,
                    AVG(light_infrared),
                    AVG(light_visible),
                    AVG(light_lux),
                    AVG(pressure),
                    AVG(temperature),
                    AVG(humidity),
                    AVG(soil_moisture)
               FROM sensor_data
               WHERE
                recorded_at >= DATETIME('NOW', '-%d Minute')''' %
             int(timeframe_minutes)),
            []
        ).fetchone()
        return result

    def get_last_light_switch_state(self):
        result = self._execute(
            '''SELECT light_switch_state
               FROM sensor_data
               ORDER BY recorded_at DESC
               LIMIT 1''',
            []
        ).fetchone()[0]
        return result

    def _execute(self, query, params):
        return self._conn.cursor().execute(query, params)
