(define (domain touristinfo)
  (:requirements :typing :fluents :durative-actions :strips :equality :negative-preconditions :timed-initial-literals :preferences :duration-inequalities) 
  (:types         location mode tourist - object
  
  )
  (:predicates 
		(at ?obj - tourist ?loc - location)
		(open ?loc - location)
		(time ?num - int)
		(visited ?tourist - tourist ?loc - location)
	                (path ?x ?y - location)
		(time-at ?loc)
)

(:functions (traveltime ?mode - mode ?loc-from ?loc-to - location)
	(visitfor ?loc - location ?tourist - tourist)
	(time-at ?loc - location))

(:durative-action MOVE
  :parameters
   (?tourist - tourist
    ?loc-from - location
    ?loc-to - location
    ?mode - mode)
  :duration (=?duration (traveltime ?mode ?loc-from ?loc-to))
  :condition
   (and (at start (at ?tourist ?loc-from)) (at start (path ?loc-from ?loc-to))) 
  :effect
   (and (at start (not (at ?tourist ?loc-from))) (at end (at ?tourist ?loc-to))))

(:durative-action VISIT
 :parameters
   (?tourist - tourist
   ?loc - location)
 :duration (>=?duration (visitfor ?loc ?tourist))
 :condition
   (and (over all (at ?tourist ?loc)) (over all (open ?loc)))
 :effect
   (and (at end (visited ?tourist ?loc)) (at end (increase (time-at ?loc) ?duration))))
 
)