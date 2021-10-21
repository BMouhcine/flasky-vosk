from flask import Flask, request, send_file
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json
import collections
import csv
from datetime import datetime as dt
import subprocess
import datetime
from collections import OrderedDict
SetLogLevel(0)
app = Flask(__name__)

def convert_time(n):
	return str(datetime.timedelta(seconds = n))

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    x = OrderedDict([('index', {})])
    jsonString = json.dumps(x)
    with open(csvFilePath, encoding='utf-8') as csvf:
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            csvReader = csv.DictReader(csvf)
            for row in csvReader:
                jsonf.write(jsonString)
                jsonf.write("\n")
                y = json.dumps(row)
                jsonf.write(y)
                jsonf.write("\n")

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

sample_rate=16000
model = Model("model")
rec = KaldiRecognizer(model, sample_rate)
rec.SetWords(True)






header = ['start_time', 'end_time', 'content']
data = []
dtime = dt.now()
dtime_formatted_win_OS = dtime.strftime('%m-%d-%Y-%H-%M-%S')
with open('ts{}.csv'.format(dtime_formatted_win_OS), 'a') as of: # pour un rollback: dtime au lieu de dtime_formatted_win_OS
	writer = csv.writer(of)
	writer.writerow(header)


@app.route("/", methods=['POST'])
def get_media_file():
	param = request.files['data']
	if param:
		filename = request.files['data'].filename + 'h'
		param.save(filename)
		jsonFilePath = hello(filename)
		json_file_2_send = send_file(jsonFilePath, as_attachment=True)
		#os.remove(jsonFilePath)
		os.remove(filename)
		return json_file_2_send
	return "Nothing processed"

def hello(filename):
  process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                            filename,
                            '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                            stdout=subprocess.PIPE)
  while True:
      data = process.stdout.read(4000)
      if len(data) == 0:
          break
      if rec.AcceptWaveform(data):
          #print(rec.Result())
          partial_res = json.loads(rec.FinalResult())
          with open('ts{}.csv'.format(dtime_formatted_win_OS), 'a') as of: # pour un rollback: dtime au lieu de dtime_formatted_win_OS
          	writer = csv.writer(of)
          	end_time = convert_time(round(partial_res['result'][-1]['end']))
          	start_time = convert_time(round(partial_res['result'][0]['start']))
          	data = []
          	data.append(start_time)
          	data.append(end_time)
          	data.append(partial_res['text'])
          	writer.writerow(data)
          #continue
      else:
      	continue
          #print(rec.PartialResult())

  csvFilePath = 'ts{}.csv'.format(dtime_formatted_win_OS)
  jsonFilePath = 'ts{}.json'.format(dtime_formatted_win_OS)
  csv_to_json(csvFilePath, jsonFilePath)
  return jsonFilePath


if __name__ == "__main__":
  app.run()
