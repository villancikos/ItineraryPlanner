(define (problem it-84543b4c-1834-463f-90ef-7de0c9506763)
        (:domain touristinfo) 
	(:objects victorias-secret rolex-boutique cartier comptoir-libanais  - location tourist1 - tourist bus walk - mode)
 	(:init 

        (at 0800 (open rolex-boutique))
        (at 1700 (not (open rolex-boutique)))
        (at 0800 (open victorias-secret))
        (at 2200 (not (open victorias-secret)))
        (at 1100 (open cartier))
        (at 2100 (not (open cartier)))
        (at 1400 (open comptoir-libanais))
        (at 2100 (not (open comptoir-libanais)))

  		(at tourist1 rolex-boutique)
  		(path victorias-secret rolex-boutique)
		(path victorias-secret cartier)
		(path victorias-secret comptoir-libanais)
		(path rolex-boutique victorias-secret)
		(path rolex-boutique cartier)
		(path rolex-boutique comptoir-libanais)
		(path cartier victorias-secret)
		(path cartier rolex-boutique)
		(path cartier comptoir-libanais)
		(path comptoir-libanais victorias-secret)
		(path comptoir-libanais rolex-boutique)
		(path comptoir-libanais cartier)
 		(=(traveltime walk victorias-secret rolex-boutique)6.85)
		(=(traveltime walk victorias-secret cartier)5.85)
		(=(traveltime walk victorias-secret comptoir-libanais)7.03)
		(=(traveltime walk rolex-boutique victorias-secret)6.57)
		(=(traveltime walk rolex-boutique cartier)1.08)
		(=(traveltime walk rolex-boutique comptoir-libanais)13.58)
		(=(traveltime walk cartier victorias-secret)5.48)
		(=(traveltime walk cartier rolex-boutique)1.0)
		(=(traveltime walk cartier comptoir-libanais)12.52)
		(=(traveltime walk comptoir-libanais victorias-secret)6.95)
		(=(traveltime walk comptoir-libanais rolex-boutique)13.8)
		(=(traveltime walk comptoir-libanais cartier)12.8)
 		(=(visitfor victorias-secret tourist1)85)
		(=(visitfor rolex-boutique tourist1)59)
		(=(visitfor cartier tourist1)81)
		(=(visitfor comptoir-libanais tourist1)47)
	)
 	(:goal
		(and
			(at tourist1 rolex-boutique)
			(preference VisitVictoriasSecret (visited tourist1 victorias-secret))
			(preference VisitRolexBoutique (visited tourist1 rolex-boutique))
			(preference VisitCartier (visited tourist1 cartier))
			(preference VisitComptoirLibanais (visited tourist1 comptoir-libanais))
		)
	)
 	(:constraints
		(and
			(preference VisitVictoriasSecret (at end (visited tourist1 victorias-secret)))
			(preference VisitRolexBoutique (at end (visited tourist1 rolex-boutique)))
			(preference VisitCartier (at end (visited tourist1 cartier)))
			(preference VisitComptoirLibanais (at end (visited tourist1 comptoir-libanais)))
		)
	) 
	(:metric minimize
		(+
			(total-time)
			(* 1000    
				(+
					(is-violated VisitVictoriasSecret)
					(is-violated VisitRolexBoutique)
					(is-violated VisitCartier)
					(is-violated VisitComptoirLibanais)
				)
			)
		)
	)
)
