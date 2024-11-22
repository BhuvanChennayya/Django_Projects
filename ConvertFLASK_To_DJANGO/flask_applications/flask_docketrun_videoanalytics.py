import Data_recieving_and_Dashboard.main_api as main_api
from Data_recieving_and_Dashboard.main_api import app
from Data_recieving_and_Dashboard.packages import *
from setproctitle import setproctitle
DB_NAME ='DOCKETRUNDB'#'TSKTEST'#'tsk01062023' #'test_security'#'DOCKETRUNDB' #'tsk2005'
main_api.set_mongodb_name(db_name=DB_NAME)
setproctitle("DOCKET-Flask_Application-5000")
# serve(app, port=5000,threads=1000)#,threaded=True)
app.run(host='0.0.0.0', port=5500, debug=True, threaded=True)

# import Data_recieving_and_Dashboard.main_api as main_api
# from Data_recieving_and_Dashboard.main_api import app
# from Data_recieving_and_Dashboard.main_api import socketio
# #from Data_recieving_and_Dashboard.main_api import socketio2
# from Data_recieving_and_Dashboard.packages import *
# from setproctitle import setproctitle
# DB_NAME ='DOCKETRUNDB'#'TSKTEST'#'tsk01062023' #'test_security'#'DOCKETRUNDB' #'tsk2005'
# main_api.set_mongodb_name(db_name=DB_NAME)
# setproctitle("DOCKET-Flask_Application-5000")
# # serve(app, port=5000,threads=1000)#,threaded=True)#use_reloader=False
# #app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

# socketio.run(app,debug=True,host='0.0.0.0',port=5000)
# socketio.run(app,host='0.0.0.0',port=5000)
# socketio.run(app,host='0.0.0.0', port=5000)
#pip3 install flask-socketio
#   820  python3 flask_docketrun_videoanalytics.py 
#   821  pip3 install gevent
#   822  python3 flask_docketrun_videoanalytics.py 
#   823  python3 main_api.py 
#   824  pip3  install gevent-websocket

