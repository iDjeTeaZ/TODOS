def DEBUG(**kwargs):
	cmd = ""
	for var in kwargs:
		exec(f"{var} = kwargs[var]")
	while cmd != "stop":
		exec(cmd)
		cmd = input("$ ")
