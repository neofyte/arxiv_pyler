try:
	raise Exception('egg')
except Exception as inst:
    print (str(inst.args))