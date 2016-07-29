// SDEH
// AHAQ

import RNG.Simple

import scala.annotation.tailrec
import scala.collection.immutable.Stream.Empty

//Tests
object test extends App {
  println(RNG.nonNegativeInt(Simple(2))._1)
  println(RNG.double(Simple(1900000000))._1)
  println(RNG.ints(10)(Simple(2))._1)
  println(RNG._double(Simple(1900000000))._1)
  println(RNG.nonNegativeLessThan(4)(Simple(1900000000))._1)
  println(State.random_int.run(Simple(42)))
  println(State.random_int.run(Simple(42)))
  println("Pre list")
  State.state2stream(State.random_int)(Simple(42)).take(5).toList.foreach(println)
  println("Post list")
  State.state2stream(State.random_int)(Simple(42)).take(10).toList.foreach(println)
}


trait RNG {
  def nextInt: (Int, RNG)
}

object RNG {
  // NB - this was called SimpleRNG in the book text

  case class Simple(seed: Long) extends RNG {
    def nextInt: (Int, RNG) = {
      val newSeed = (seed * 0x5DEECE66DL + 0xBL) & 0xFFFFFFFFFFFFL // `&` is bitwise AND. We use the current seed to generate a new seed.
      val nextRNG = Simple(newSeed) // The next state, which is an `RNG` instance created from the new seed.
      val n = (newSeed >>> 16).toInt // `>>>` is right binary shift with zero fill. The value `n` is our new pseudo-random integer.
      (n, nextRNG) // The return value is a tuple containing both a pseudo-random integer and the next `RNG` state.
    }
  }

  // Exercise 1 (CB 6.1)
  @tailrec
  def nonNegativeInt(rng: RNG): (Int, RNG) = {
    val nxt = rng.nextInt
    nxt._1 match {
      case Int.MinValue => nonNegativeInt(nxt._2) //Give another go
      case x if x < 0 => (x * -1, nxt._2)
      case _ => nxt
    }
  }

  // Exercise 2 (CB 6.2)

  def double(rng: RNG): (Double, RNG) = {
    val nni = nonNegativeInt(rng)
    (nni._1 / (Int.MaxValue.toDouble + 1), nni._2)
  }

  // Exercise 3 (CB 6.3)

  def intDouble(rng: RNG): ((Int, Double), RNG) = {
    val nni = nonNegativeInt(rng)
    val dou = double(nni._2)

    ((nni._1,dou._1), dou._2)
  }

  def doubleInt(rng: RNG): ((Double, Int), RNG) = {
    val dou = double(rng)
    val nni = nonNegativeInt(dou._2)

    ((dou._1,nni._1), nni._2)
  }

  def double3(rng: RNG): ((Double, Double, Double), RNG) = {
    val d1 = double(rng)
    val d2 = double(d1._2)
    val d3 = double(d2._2)

    ((d1._1, d2._1, d3._1), d3._2)
  }

  // def boolean(rng: RNG): (Boolean, RNG) =
  //  rng.nextInt match { case (i,rng2) => (i%2==0,rng2) }

  // Exercise 4 (CB 6.4)

  def ints(count: Int)(rng: RNG): (List[Int], RNG) = count match {
    case x if x > 0 => {
      val nxt = rng.nextInt
      val ls = ints(x-1)(nxt._2)
      (nxt._1::ls._1, ls._2)
    }
    case _ => (Nil, rng)
  }

  // There is something terribly repetitive about passing the RNG along
  // every time. What could we do to eliminate some of this duplication
  // of effort?

  type Rand[+A] = RNG => (A, RNG)

  val int: Rand[Int] = _.nextInt

  def unit[A](a: A): Rand[A] =
    rng => (a, rng)

  def map[A,B](s: Rand[A])(f: A => B): Rand[B] = rng => {
    val (a, rng2) = s(rng)
    (f(a), rng2)
  }

  // def nonNegativeEven: Rand[Int] = map(nonNegativeInt)(i => i - i % 2)

  // Exercise 5 (CB 6.5)

  val _double: Rand[Double] = map(nonNegativeInt)(i => i / (Int.MaxValue.toDouble + 1))

  // Exercise 6 (CB 6.6)

  def map2[A,B,C](ra: Rand[A], rb: Rand[B])(f: (A, B) => C): Rand[C] =  rng => {
    val (a, rn) = ra(rng)
    val (b, rn2) = rb(rn)
    (f(a,b), rn2)
  }

  // this is given in the book

  // def both[A,B](ra: Rand[A], rb: Rand[B]): Rand[(A,B)] =
  //  map2(ra, rb)((_, _))

  // val randIntDouble: Rand[(Int, Double)] = both(int, double)

  // val randDoubleInt: Rand[(Double, Int)] = both(double, int)

  // Exercise 7 (6.7)
  //TODO
  //def sequence[A](fs: List[Rand[A]]): Rand[List[A]] =

  // def _ints(count: Int): Rand[List[Int]] = ...

  // Exercise 8 (6.8)

  def flatMap[A,B](f: Rand[A])(g: A => Rand[B]): Rand[B] = rng => {
    val fr = f(rng)
    g(fr._1)(fr._2)
  }

  def nonNegativeLessThan(n: Int): Rand[Int] = flatMap(nonNegativeInt)(x => unit(x % n))

  // Exercise 9 (6.9)

  def _map[A,B](s: Rand[A])(f: A => B): Rand[B] = flatMap(s)(a => unit(f(a)))

  def _map2[A,B,C](ra: Rand[A], rb: Rand[B])(f: (A, B) => C): Rand[C] = flatMap(ra)(a => _map(rb)(b => f(a,b)))
}

import State._

case class State[S, +A](run: S => (A, S)) {

  // Exercise 10 (6.10)

  def map[B](f: A => B): State[S, B] = flatMap(a => unit(f(a)))

  def map2[B,C](sb: State[S, B])(f: (A, B) => C): State[S, C] = flatMap(a => sb.map(b => f(a,b)))

  def flatMap[B](f: A => State[S, B]): State[S, B] = State(s => {
    val fs = run(s)
    f(fs._1).run(fs._2)
  })

}

object State {
  type Rand[A] = State[RNG, A]

  def unit[S, A](a: A): State[S, A] =
    State(s => (a, s))

  // Exercise 10 (6.10) continued
  // TODO
  // def sequence[S,A](sas: List[State[S, A]]): State[S, List[A]] = ...
  //
  // This is given in the book:

  // def modify[S](f: S => S): State[S, Unit] = for {
  //   s <- get // Gets the current state and assigns it to `s`.
  //   _ <- set(f(s)) // Sets the new state to `f` applied to `s`.
  // } yield ()

  def get[S]: State[S, S] = State(s => (s, s))

  def set[S](s: S): State[S, Unit] = State(_ => ((), s))


  def random_int :Rand[Int] =  State (_.nextInt)

  // Exercise 11

  def state2stream[S,A] (s :State[S,A]) (seed :S) :Stream[A] = {
    val (x,y) = s.run(seed)
    Stream.cons(x, state2stream(s)(y))
  }

  // Exercise 12

  val random_integers = state2stream(State.random_int)(Simple(42)).take(10).toList

}






sealed trait Input
case object Coin extends Input
case object Turn extends Input

case class Machine(locked: Boolean, candies: Int, coins: Int)

// Exercise 13 (CB 6.11)
//object Candy {
//  def update = (i: Input) => (s: Machine) =>
//    (i, s) match {
//      case (_, Machine(_, 0, _)) => s
//      case (Coin, Machine(false, _, _)) => s
//      case (Turn, Machine(true, _, _)) => s
//      case (Coin, Machine(true, candy, coin)) =>
//        Machine(false, candy, coin + 1)
//      case (Turn, Machine(false, candy, coin)) =>
//        Machine(true, candy - 1, coin)
//    }

  //def simulateMachine(inputs: List[Input]): State[Machine, (Int, Int)] = for {
  //  _ <- sequence(inputs map (modify[Machine] _ compose update))
  //  s <- get
  //} yield (s.coins, s.candies)
//}

// vim:cc=80:foldmethod=indent:foldenable
