// Advanced Programming 2015
// Andrzej Wasowski, IT University of Copenhagen
// Exercises/Miniproject/Tutorial on lenses.
//
// Monocle is a library providing lenses for Scala (one of many in fact)
//
// Tutorial for Monocle lenses is here:
// https://github.com/julien-truffaut/Monocle/blob/master/docs/src/main/tut/lens.md
//
// We will reimplement some Lenses today, but we shall reuse some basic
// infrastructure from Monocle.  Monocle is *probably* the most popular Lens
// framework for scala, although scalaz provides its own lenses, and so does
// shapeless.
//
// Documentation is sparse so far, but the source code is here:
// https://github.com/julien-truffaut/Monocle/tree/v1.2.0-M1
//
// And some examples are here (and in other files in the same directory):
// https://github.com/julien-truffaut/Monocle/blob/master/example/src/test/scala/monocle/LensExample.scala
//
// We are now advanced enough in Scala and functional programming to understand
// a lot of it :)
//
// Work through this file in the order of numbered exercises (top to bottom),
// referring to LensesSpec.scala whenever necessary.
//
// Some notes:
//
// 1. Put is called Set in Monocle (and virtually all lens implementations)
//
// 2. Put/Set is curried ([Morries 2012] has a discussion that touches on
//    advantages of currying set)
//
// 3. Total lenses are called Lens in monocle.  Partial lenses are of type
//    Optional.

package adpro

import monocle.std.set

import scala.concurrent.duration.DurationConversions.fromNowConvert.R
import scalaz._
import monocle.{Lens, Optional}
import monocle.PLens._
import monocle.std.map._
import monocle.std.map.mapIndex
import monocle.syntax._
import monocle.function.{index, each, filterIndex}

object Lenses {

  // Exercise 0. Study the implementation of lens l1 below and compare it to the
  // first example in Foster et al. (Page 6).
  // page 6 in Foster et al.

  val l1 = Lens[(String, Int), String](_._1)(s1 => _ => (s1, 0))

  // Complete the second example from page 6, and the example from page 7 below:

  // page 6 in Foster et al.:

  val l2 = Lens[String, (String, Int)]((_, 0))(s => _ => s._1)

  // page 7 in Foster et al.
  val l3 = Lens[(String, Int), String](_._1)(s => s1 => if (s == s1._1) (s, s1._2) else (s, s1._2 + 1))


  // Exercise 1: Write PutGet law as a property test for arbitrary lenses from
  // type C to typ A; do the same for GetPut and PutPut.  Test the above three
  // lenses and find in the paper whether the results are consistent. Put the
  // tests in LensesSpec.scala in the tests directory.

  // In general it may be difficult to prove mathematically that your lenses
  // obey the good laws, but ... we can cheat :)  There is always property testing!
  // With some plumbing we can even use the implementations of the tests
  // provided by the framework (See the bottom of LensesSpec.scala... but in
  // this exercise please implement your tests from scratch).


  // Exercise 2: Implement the lens coding from Either[A.A] to A (this is
  // presented by [Morris, 2012]. This may be thought of as taking either A or A
  // and stripping the choice of A from the Either value. The type of this value
  // is Lens[Either[A, A], A].
  //
  // Monocle prefers to use A \/ B instead od Either[A,B].  This is practically
  // the same thing (\/ is introduced by scalaz, and Either comes in the
  // standard library). "-\/" is the name of the left constructor and "\/-" is
  // the name of the right constructor (you can pattern match against them). We
  // use the infix constructor in this exercise, instead of Either.  All the
  // imports in the project are already set up.

  def set[A](a: A)(a1: A \/ A): A \/ A = a1 match {
    case -\/(a1) => -\/(a)
    case \/-(a1) => \/-(a)
  }

  def get[A](a: A \/ A): A = a match {
    case -\/(a) => a
    case \/-(a) => a
  }

  def codiag[A]: Lens[A \/ A, A] = Lens[A \/ A, A](get)(set)

  //
  // Some codiag tests are found in LensesSpec.  Test your solution.

  // Exercise 3: Section 5.3 of [Morris  2012] describes a choice combinator for
  // lenseis |||: Lens[R, F] => Lens[S, F] => Lens[Either[R, S], F].
  //
  // Morris uses it to implement the above codiag lense together with an
  // identity lense (Identity is described in [Foster et al. p 12] and in
  // [Morris p.3 Listing 12].
  //
  // In Monocle '|||' is called "lensChoice.choice" and identity is called
  // "Lens.id", the same way as Morris calls it. Observe also that Monocle's
  // setters are curried, while Morris's are not.
  //
  // Translate morris' implementation of codiag to Monocle and test it.

  def codiag1[A]: Lens[A \/ A, A] = {
    lensChoice.choice(Lens.id, Lens.id)
  }

  //
  // Test this implementation uncommenting tests in LensesSpec.scala


  // Exercise 4: (Important: this exercise shows the main application of lenses)
  //
  // Consider the following types:

  type ZipCode = String
  type Name = String
  type Students = Map[Name, Address]

  case class Address(val zipcode: ZipCode, val country: String)

  case class University(val students: Students, val address: Address)

  // and an example data value:

  val itu = University(Map(
    "Stefan" -> Address("2300", "Denmark"),
    "Axel" -> Address("91000", "France"),
    "Alex" -> Address("2800", "Denmark"),
    "Christian" -> Address("D-4242", "Germany"),
    "Andrzej" -> Address("00-950", "Poland"),
    "Thorsten" -> Address("6767", "Sweden")
  ), Address("2300", "Amager")
  )

  // Write an expression that modifies "itu" in such a way that Alex is in
  // Denmark but at post-code 9100. First without using lenses.
  //
  // Hint: every class in Scala has a method called 'copy' that takes the same
  // parameters as the constructor.  All parameters are optional.  Use the name
  // assignment convention to only change values of properties that you want in
  // the copy.  For instance itu.copy (students = itu.students.tail) creates a
  // copy of ITU without the first student.

  val itu1 = itu.copy(itu.students.updated("Alex", Address("9100", itu.students.get("Alex").get.country)))

  // There is a test in LensesSpec to check whether  you did what expected.
  //
  // As you see doing this without lenses is very very annoying.  Updating
  // nested properties in complex objects is much easier in imperative
  // programming.


  // Exercise 5.  Lenses to the rescue.  Try to extend our hypothetical
  // university library with lenses, so that using the types is almost as
  // natural as in imperative languages.
  //
  // a) design a lense that accesses zipcode from Address objects:

  val _zipcode: Lens[Address, ZipCode] = Lens[Address, ZipCode](_.zipcode)(z => a => a.copy(zipcode = z, a.country))

  // b) design a lense that accesses the students collection from university:

  val _students: Lens[University, Students] = Lens[University, Students](_.students)(s => a => a.copy(students = s))

  // c) Use the following index lense (name)  from Monocle:

  index("Alex"): Optional[Map[String, Address], Address]

  // This lens focuses our view on the entry in a map with a given index.
  // Optional in the Monocle terminology is a partial lense in the terminology
  // of Foster et al.
  //
  // Use lenses compositin to update itu the same way as above but in a clearer
  // way (use the infix binary operator ^|-? to compose a lense with an
  // optional, and use ^|-> to compose the optional with a lense).
  val itu2: University = (_students ^|-? index("Alex") ^|-> _zipcode).modify(_ => "9100")(itu)

  // There is a test in LensesSpec to test whether what you have built behaves
  // as expected.
  //
  // Now once you provide lenses for your types, navigating and modifying deep
  // structures becomes more readable and easier to write.  In fact, lense
  // libraries provide various mechanisms to generate them for the properties of
  // your case classess, so this access can come at almost no (coding) cost.


  // Exercise 6. We shall now turn upper case names of all countries in all the
  // addresses of all students in the itu object.
  //
  // We shall use the 'modify' function of lenses. Morris describes modify
  // problem in Section 2, and shows the lens solution in Listing 9.  Monocle
  // has a modify method in Lens[A.B]:
  //
  // modify : (B => B) => A => A
  //
  // It works almost like get and set at the same time (so you use modify if you
  // would otherwise like to get a value, and then make a modification to this
  // value).  Modify takes a function that makes the change (computes the new
  // data) and then the source(concrete) object.  It returns the new object. It
  // is potentially more efficient than using get and set separately.
  //
  // In this exercise we will use modify to perform a cross cutting modification
  // on a complex structure.
  //
  // We will need a lense that gives us all countries from the map of students.
  // This kind of lense is called a Traversable in Monocle.
  //
  // We use infix ^|->> to compose an optical (Lens, Traversable, Optional, etc)
  // with a traversable (as we use ^|-> to compose any of these with a Lens).
  //
  // The traversable "each" (which has a default instance for maps) will give us
  // a collection of all objects (values in a map).  So to solve the task we
  // need to compose:
  //
  // - a lense that extracts the students collection from a University
  //(_students)
  //
  // - a traversable that extracts all objects from a collection (each)
  //
  // - a lense that extract the country from an address object (_address, you
  // will need to write that one, as we did not create it yet).

  val _country: Lens[Address, String] = Lens[Address, String](_.country)(c => a => a.copy(a.zipcode, country = c))
  //
  val itu3: University = (_students ^|->> (each) ^|-> _country).modify(_.toUpperCase)(itu)

  // LensesSpec.scala has a test to see if you succeeded.
  //
  // QUESTION: Compare the test with the code used above.  Why have we used
  // lenses/traversals above, and not in the test? What is the difference
  // between the code in the test and the code above that influences this? Write
  // the answer below:
  //
  // The code in the test only iterate through the values and compare if they are uppercase,
  // while Lenses actually are able to change the value, and keeping the original structure.
  // If you want like to modify the object without lenses, you would need to use the copy method.


  // Exercise 7. Use filterIndex(p) to only capitalize city names of the
  // students on the list whose name satisfies predicate (p).  filterIndex is a
  // traversal, like 'each' above. Recall that ^|->> is used to compose (append)
  // a traversal and ^|-> is used to append a lense.

  val itu4: University = (_students ^|->> filterIndex((x: String) => x.startsWith("A")) ^|-> _country).modify(_.toUpperCase)(itu)

  println(itu4)

  //[cheap testing]


  // Exercise 8.  We are returning to construction of basic lenses.  Implement a
  // (partial) lens that accesses ith element of a list (let's call it index).
  // A partial lens, so a Optional in Monocle terminology, would be of type
  // Optional[List[A],A].  The Optional takes two parameters for the
  // constructor:
  //
  // get: List[A] => Option[A]
  // set: A => List[A] => List[A]
  //
  def setIth[A](n: Integer): Optional[List[A], A] =
    Optional[List[A], A](_.lift(n-1))(a => l => if (l.size < n) l else l.updated(n-1, a))


  // In the above you will need to decide what to do with the setter if n is
  // greater than the length of the list.  One option is to do nothing, jus
  // ignore the setting :).  Another alternative is to provide a default
  // element, and extend the list approprietly. In such case we obtain a total
  // lense. Try this too:

  def setIth1[A](n: Integer, default: A): Lens[List[A], A] =
    Lens[List[A], A](_.lift(n-1).orElse(Some(default)).get)(a => l => if(l.size<n) {
      (l ++ List.fill((n - l.size))(default)).updated(n-1,a)

    }else
      l.updated(n-1, a)
    )
  // Exercise 9. To test setIth (above) you will also need to implement new
  // PutGet, GetPut and PutPut laws that work for Optionals. Add the tests to
  // LensesSpec.scala.  Carefully consider the equality of results as used in
  // Foster et al. (The \sqsubseteq ordering)
  //
  // Test setIth1 with existing laws that you have already used for your earlier
  // lenses (setIth1 is a usual total lense).
  //
  // Proceed in LensesSpec.scala


  // Exercise 10.  setIth demonstrates that lenses emulate a form of
  // "imperative" programming, by making a structure updatedable, even deeply.
  // For a simple example, use sethIth below to increment the third element on a
  // list list0

  val list0 = List[Int](1,2,3,4,5,6)
  val list1 = (setIth(3)).modify((a:Int)=>a+1)(list0)
  println (list0)
  println (list1)

}


