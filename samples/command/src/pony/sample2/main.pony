// This file is a "Hello, world!" in Pony language for wandbox.

actor Main
  new create(env: Env) =>
    env.out.print("Hello, Wandbox!")

    let test2 = Test2(env)

// Pony language references:
//   http://www.ponylang.org/
