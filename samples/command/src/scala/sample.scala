// This file is a "Hello, world!" in Scala language for wandbox.
import scala.language.postfixOps
import test1._
import _root_.test3.Test3, test4.Test4; import test4.{Test05 => Test5}

object Wandbox {
  def main(args: Array[String]): Unit = {
    println("Hello, Wandbox!")
    new test1.Test1().test()
    new test1.Test2().test()
    new Test3().test()
    new Test4().test()
    new Test5().test()
  }
}

// Scala language references:
//   http://www.scala-lang.org
