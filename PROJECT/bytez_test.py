from bytez import Bytez

key = "95e3d425613b1c1736a910b4c1512339"
sdk = Bytez(key)

# choose gemini-2.5-flash-lite
model = sdk.model("google/gemini-2.5-flash-lite")

# send input to model
results = model.run([
  {
    "role": "user",
    "content": "Hello"
  }
])

print({ "error": results.error, "output": results.output })
