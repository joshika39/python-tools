class BotAction():
	exit_after = False

	def __init__(self, name, action, exit_after=False):
		self.name = name
		self.action = action
		self.exit_after = exit_after

	def do_action(self, *args):
		print(f"Given args: {len(args)} ({args})")
		self.action(list(args))