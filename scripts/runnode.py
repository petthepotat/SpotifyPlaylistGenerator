import subprocess

# Read the Node.js script
node_script = open("scripts/runnode.js", "r").read()

# Create a Node.js process
process = subprocess.Popen(["node", "-e", node_script], stdout=subprocess.PIPE)

# Read the output of the Node.js process
output, error = process.communicate()

# Print the output of the Node.js process
print(output.decode().strip())



