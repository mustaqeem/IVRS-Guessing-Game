from flask import Flask, make_response, request
import plivo, plivoxml, json, random
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    auth_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    auth_token = "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
    p = plivo.RestAPI(auth_id, auth_token)
    params = {
    'from': '1800111108', # Caller Id
    'to' : '917829715262', # User Number to Caller
    'answer_url' : "http://your_server/answer_url",
    'answer_method' : 'GET',
    'hangup_url':'http://your_server/do_nothing'
    }
    response = p.make_call(params)
    return str(response)


@app.route('/answer_url',methods=['GET','POST'])
def answer_url():
    rand = random.randint(0,9)
    print '\nGenerated Random Number '+str(rand)+'\n'
    r = plivoxml.Response()
    params = {'action':'http://your_server/action?rand='+str(rand)+'&rem=4','method':'GET','numDigits':1,'playBeep':'true'};
    gd = r.addGetDigits(**params)
    gd.addSpeak(body = 'You have 4 chances')
    gd.addSpeak(body = 'Choose from 0 to 9')
    response = make_response(r.to_xml())
    response.headers["Content-type"] = "text/xml"
    return response

@app.route('/action',methods=['GET','POST'])
def action():
    rand = request.args['rand']
    rem = int(request.args['rem'])
    d = request.args['Digits']
    if rem > 1:
        if d == rand:
            body = 'You win'
        else:
            body = 'Wrong'
            if d > rand:
                body += ' Choose less'
            else:
                body += ' Choose more'
    else:
        body = 'Sorry, no remaining chance. You lose'
    r = plivoxml.Response()
    r.addSpeak(body)
    if body.startswith('Wrong'):
        params = {'action':'http://your_server/action?rand='+str(rand)+'&rem='+str(rem-1),'method':'GET','numDigits':1,'playBeep':'true'};
        gd = r.addGetDigits(**params)
        gd.addSpeak(body = 'You have '+str(rem-1)+' remaining chances. Choose another number')
    response = make_response(r.to_xml())
    response.headers["Content-type"] = "text/xml"
    return response

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)