(define (problem itinerary-d41c8390-38ca-4489-9671-c92f4d482519)
        (:domain touristinfo) 
	(:objects piccadilly-circus temple-station  - location tourist1 - tourist bus walk - mode)
 	(:init 
 		(at 0 (open piccadilly-circus))
		(at 0 (not (open piccadilly-circus)))
		(at 0 (open temple-station))
		(at 0 (not (open temple-station)))
 		(at tourist1 temple-station)
 		(path piccadilly-circus temple-station)
		(path temple-station piccadilly-circus)
 		(=(traveltime walk piccadilly-circus temple-station)20.53)
		(=(traveltime walk temple-station piccadilly-circus)21.45)
 		(=(visitfor piccadilly-circus tourist1)79)
		(=(visitfor temple-station tourist1)66)
	)
 	(:goal
		(and
			(at tourist1 temple-station)
			(preference VisitPiccadillyCircus (visited tourist1 piccadilly-circus))
			(preference VisitTempleStation (visited tourist1 temple-station))
		)
	)
 	(:constraints
		(and
			(preference VisitPiccadillyCircus (at end (visited tourist1 piccadilly-circus)))
			(preference VisitTempleStation (at end (visited tourist1 temple-station)))
		)
	) 
	(:metric minimize
		(+
			(total-time)
			(* 1000    
				(+
					(is-violated VisitPiccadillyCircus)
					(is-violated VisitTempleStation)
				)
			)
		)
	)
)
