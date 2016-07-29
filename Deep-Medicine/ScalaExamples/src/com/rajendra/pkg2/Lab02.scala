package com.rajendra.pkg2

object Lab02 {
  abstract class Duck {
    def display(): String

    def swim() {
      println("All ducks float, even decoys!")
    }
  }

  class ModelDuck extends Duck {
    // FIXME
    // override the display method
    // remember that 'override' is a keyword and is required in Scala
    override def display(): String = "Inside ModelDucke class"
  }

  // FIXME
  // add Mixins FlyNoWay and Squeak to the rubber duck
  class RubberDuck extends Duck with Fly with Quack { // FIXME
    override def display(): String = "Inside RubberDuck class"
  }

  // FIXME
  // define subclass MallardDuck with Mixins Fly and Quack
  class MallardDuck extends Duck with Fly with Quack { // FIXME
    override def display(): String = "Inside MallardDuck class"
  }

  trait Fly {
    def fly() = {
      "I'm flying"
    }
  }

  trait FlyRocketPowered {
    def fly() = {
      "I'm flying with a rocket"
    }
  }

  trait FlyNoWay {
    def fly() = {
      "I can't fly"
    }
  }

  trait Quack {
    def quack() = {
      "Quack"
    }
  }

  trait MuteQuack {
    def quack() = {
      "<< Silence >>"
    }
  }

  trait Squeak {
    def quack() = {
      "Squeak";
    }
  }

}