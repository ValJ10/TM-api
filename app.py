from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

# Assuming dbs is in your app root folder
fixtures = create_engine('sqlite:///Fixtures.db')
app = Flask(__name__)
api = Api(app)

class LeagueList(Resource):
    def get(self):
        conn = fixtures.connect()
        query = conn.execute('select "Code" from Leagues')
        resultset = {'Leagues': [i[0] for i in query.cursor.fetchall()]}
        conn.close()
        return resultset


class Fixtures(Resource):
    def get(self,leagueCode):
        conn = fixtures.connect()
        query = conn.execute("select Date, HomeTeam, AwayTeam, FTHG, FTAG , HTHG, HTAG, HTR, FTR From '%s'"%leagueCode)
        
        rows =  ((query.cursor.fetchall()))
        result =[]
        for row in rows:
            result.append({'Date':row[0],
                           'HomeTeam':row[1],
                           'AwayTeam':row[2],
                           'Full Time Home Goals':row[3],
                           'Full Time Away Team Goals':row[4],
                           'Half Time Home Team Goals':row[5],
                           'Half Time Away Team Goals' : row[6],
                           'Half Time Result': row[7],
                           'Full Time Result':row[8]
                           })
        conn.close()
        return result

# Routes
api.add_resource(LeagueList,'/leagues')
api.add_resource(Fixtures,'/fixture/<string:leagueCode>')

if __name__ == '__main__':
    app.run(debug=True)
