import json, os, functools
from .utils import get_current_time_seconds, parse_int, parse_bool
from datetime import timedelta
from types import SimpleNamespace
from flask import jsonify, request
from flask_jwt_extended import *
from scrypt import hash
from .models import db, User

current_app= None
ENV = "dev" if os.environ.get("FLASK_DEBUG", "0") == "1" else "prod"

CONTENT_TYPE_JSON= {'Content-Type': 'application/json'}
CONTENT_TYPE_MULTIPART= {'Content-Type': 'multipart/form-data'}

##--- common configurable tests for endpoints, just to avoid writing it everytime
#def endpoint_safe(f, shell):
#  #try:
#    body= None 
#    data= {}
#    # force content to be given type
#    if 'content' in shell.options:
#      content= shell.options["content"]
#      if not 'Content-Type' in request.headers or not request.headers['Content-Type'] == content: return response(400, f"Content-Type is not '{content}'")
#      if 'data' in shell.options: return response(400, "cannot define shell data-type if content-type is beign defined")
#      if content == 'application/json':
#        if not request.data: return response(400, "body must contain data")
#        body= "json"
#      if content == 'multipart/form-data':
#        if not request.form and not request.files: return response(400, "body must contain data")
#        body= "multipart"
#    elif 'data' in shell.options: body= shell.options['data']
#    # load data automatically
#    if body=="json":
#      try: data['json']= request.get_json(force=True)
#      except: return response(400, "body contains no valid JSON")
#      if not data['json']: return response(400, "body contains no JSON")
#    if body=="multipart":
#      try: data['json']= json.loads(request.form['json'])
#      except: pass
#      try: data['files']= request.files
#      except: pass
#      if not data['json'] and not data['files']: return response(400, "body contains no data")
#    # check missing or invalid properties
#    if 'props' in shell.options:
#      if not data['json']: return response(400, "given required properties but no data received")
#      props= shell.options["props"]
#      json= data['json']
#      for p in props:
#        if not p in json: return response(400, f"missing required property '{p}'")
#        if not json[p] or (type(json[p])== str and json[p]== ""): return response(400, f"empty required property '{p}'")
#      if 'props_strict' in shell.options and len(json.keys()) > len(props): return response(400, f"json contains extra garbage properties")
#    # execute the endpoint function if everything else went right
#    shell.data= SimpleNamespace(**data)
#    return f(shell)
#  #except Exception as e:
#  #  print(e)
#  #  return response_500(repr(e))

#--- check a list of properties against data
def check_missing_properties_manual(data, props):
  for p in props:
    if not p in data:
      return f"missing required property '{p}'"
  return None

def get_shell(locals, **options): return SimpleNamespace(**{ "namespace": SimpleNamespace(**locals), "data": {}, "options": options})

def response(status:int, msg:str, data=None, debug=None) -> tuple[dict, int, dict]:
  obj= { "msg": msg }
  if data: obj['res']= data
  if debug: obj['_']= json.loads(json.dumps(debug, default=json_object_safe))
  return jsonify(obj), status, CONTENT_TYPE_JSON

def response_200(data=None, debug=None): return response(200, "ok", data, debug)
def response_201(data=None, debug=None): return response(201, "created", data, debug)
def response_400(data=None, debug=None): return response(400, "bad request", data, debug)
def response_401(data=None, debug=None): return response(401, "unauthorized", data, debug)
def response_403(data=None, debug=None): return response(403, "forbidden", data, debug)
def response_500(data=None, debug=None): return response(500, "server error", data, debug)

def json_object_safe(obj):
  dict= obj.__dict__
  return dict if dict else type(obj).__name__

#--- get the user by acount
def get_user_by_username_or_email(account):
  user= get_user(account, account)
  mode= None
  if user: mode= 1 if user.username==account else 2
  return user, mode

#--- get the user with given username and email
def get_user(username=None, email=None):
  user= User.query.filter(User.email==email or User.username==username).first()
  return user

#--- get the user by current jwt identity
def get_user_by_identity():
  try:
    identity= get_jwt_identity()
    user= User.query.filter(User.email==identity['e'] or User.username==identity['u']).first()
    if not user: None, response(400, "invalid or expired session")
  except Exception as e: return None, response_500(repr(e))
  return user, None

#--- check the user's login
def get_user_login(account, password):
  user, _= get_user_by_username_or_email(account)
  if not user: return None, response(400, "invalid credentials")
  # bad password returns a 401 unauthorized instead of 400 bad request just so we can do a fast check to prompt a "forgot password" shit in frontend
  if not check_password(password, user.password): return None, response(401, "invalid password")
  return user, None

#--- create both refresh and access tokens for a given user -- called ONLY on login
def create_new_tokens(user, remember):
  identity= {"u":user.username, "e":user.email, "p":user.permission, "t":user.timestamp}

  create_new_refresh_token(identity, remember)
  return create_new_access_token(identity)

#--- checks and tries to rotate (renew) the tokens automatically if their expiry date is coming
def test_rotate_tokens(apayload, identity):
  
  # refresh token
  target_timestamp = get_current_time_seconds() + timedelta(minutes=30)
  user= get_user(identity['u'], identity['e'])
  if user and user.refreshtoken:
    rpayload= decode_token(str(user.refreshtoken, 'utf-8'))
    if target_timestamp > rpayload['exp']:
      create_new_refresh_token(identity, rpayload['r'])

  # access token
  target_timestamp = get_current_time_seconds() + timedelta(minutes=5)
  if target_timestamp > apayload['exp']:
    return create_new_access_token(identity)

#--- creates a new refresh token
def create_new_refresh_token(identity, remember):
  # refresh token -- lifespan: 30 days if 'remember', 16 hours if not
  rtoken = create_refresh_token(identity, additional_claims={'r':remember}, expires_delta=None if remember else timedelta(hours=16)) # expires= None means 30 days by our jwt settings
  user= get_user(identity['u'], identity['e'])
  if user:
    user.refreshtoken= bytes(rtoken, 'utf-8')
    db.session.commit()

#--- creates a new access token
def create_new_access_token(identity):
  # access token -- lifespan: 15 min
  response= jsonify({})
  atoken = create_access_token(identity)
  return set_access_cookies(response, atoken, max_age=timedelta(minutes=15)) # access token is saved on cookie, if not 'remember', its deleted on session end (navigator close)

#--- check valid access for a token and returns the user
def get_user_with_check_access(identity=None):
  if not identity: 
    identity = get_jwt_identity()
    if not identity: return None, response_401() # unauthorized -- NOT logged-in
  user= User.query.filter((User.username==identity['u'] and User.email==identity['e'])).first()
  if not user: return None, response(400, "bad token") # shouldn't ever happen
  t= parse_int(identity['t'])
  if t is None: return None, response(400, "bad timestamp") # shouldn't ever happen
  if user.timestamp==0 or t < user.timestamp: None, response(401, "expired", {"token":t, "user":user.timestamp})
  return user, None

#--- check valid access for a token
def check_user_forbidden(level=0):
  user_identity = get_jwt_identity()
  if not user_identity: return response_401() # unauthorized -- NOT logged-in
  _, error= get_user_with_check_access(user_identity)
  if error: return error
  if user_identity['p'] < level: return response_403() # forbidden -- NOT allowed
  return None
    
#--- encrypt a password
def hash_password(password):
  return hash(password, current_app.config["JWT_SECRET_KEY"])

#--- test a password
def check_password(input, hashed):
  if input == str(hashed): return True
  _new_hash= hash(input, current_app.config["JWT_SECRET_KEY"])
  return _new_hash == hashed

#--- custom decorator, a safe endpoint wrapper and data retriever
# wrapper version of the one commented above
def endpoint_safe(
    content_type: str = None,
    data_type: str = None,
    required_props: tuple = None,
    props_strict: bool = False,
    required_params: tuple = None,
    params_strict: bool = False
) -> any:
  
  def wrapper(fn):
    @functools.wraps(fn)
    def decorator(*args, **kwargs):

      __parsed_data__= {}
      __type= data_type
      
      try:
        if content_type: # check for content_type
          if not 'Content-Type' in request.headers or not request.headers['Content-Type'] == content_type: return response(400, f"Content-Type is not '{content_type}'")
          if __type: return response(400, "cannot define shell data-type if content-type is beign defined")
          if content_type == 'application/json':
            if not request.data: return response(400, "body must contain data")
            __type= "json"
          elif content_type == 'multipart/form-data':
            if not request.form and not request.files: return response(400, "body must contain data")
            __type= "multipart"
        if __type:
          if __type=="json": # parse json
            try: __parsed_data__['json']= request.get_json(force=True)
            except: return response(400, "body contains no valid JSON")
            if not __parsed_data__['json']: return response(400, "body contains no JSON")
          if __type=="multipart": # parse multipart json + files
            try: __parsed_data__['json']= json.loads(request.form['json'])
            except: pass
            try: __parsed_data__['files']= request.files
            except: pass
            if __parsed_data__['json'] and not __parsed_data__['files']: return response(400, "body contains no data")
          if required_props: # check required json properties
            if not __parsed_data__['json']: return response(400, "given required properties but no data received")
            __json= __parsed_data__['json']
            for p in required_props:
              if not p in __json: return response(400, f"missing required property '{p}'")
              if not __json[p] or (type(__json[p])== str and __json[p]== ""): return response(400, f"empty required property '{p}'")
            if props_strict and len(__json.keys()) > len(required_props): return response(400, f"too many json properties")
        if required_params: # check required url parameters
          __params= {}
          for p in required_params:
            if not p in request.args: return response(400, f"missing required url parameter '{p}'")
            if not request.args[p] or (type(request.args[p])== str and request.args[p]== ""): return response(400, f"empty required url parameter '{p}'")
            __params[p]= request.args[p]
          if params_strict and len(__params.keys()) > len(required_params): return response(400, f"too many url parameters")
          __parsed_data__['params']= __params

        return current_app.ensure_sync(fn)(*args, **kwargs, **__parsed_data__) # execute the actual endpoint function
      
      except Exception as e: # any unhandled error (even in endpoint function) ends up here
        print(e)
        return response_500(repr(e))
      
    return decorator

  return wrapper

#--- custom decorator, the inverse of jwt_required
def jwt_forbidden(
    status: int = 401,
    message: str = "auth forbidden"
) -> any:
  
  def wrapper(fn):
    @functools.wraps(fn)
    def decorator(*args, **kwargs):
      if verify_jwt_in_request(optional=True): return response(status, message)
      return current_app.ensure_sync(fn)(*args, **kwargs)

    return decorator

  return wrapper
