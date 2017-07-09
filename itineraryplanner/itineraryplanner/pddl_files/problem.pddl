(define (problem test-tourist)
	(:domain touristinfo)
	(:objects ldneye stp trafalgsq hotel - location tourist1 - tourist bus walk - mode)
	(:init 
			(at 0600 (open stp))
			(at 1200 (not (open stp)))
	       	(at 0 (open ldneye))
	       	(at 1000 (not (open ldneye)))
	       	(at 0 (open trafalgsq))
	
	        	(at tourist1 hotel)
	        	
				(path hotel ldneye)
	        	(path hotel stp)
	        	(path hotel trafalgsq)
	        	(path ldneye stp)
	        	(path ldneye hotel)
	        	(path ldneye trafalgsq)
	        	(path stp hotel)
	        	(path stp ldneye)
				(path stp trafalgsq)
				(path trafalgsq stp)
				(path trafalgsq ldneye)
				(path trafalgsq hotel)

	        	(=(traveltime bus stp ldneye)10)
	        	(=(traveltime bus ldneye stp)10)
	        	(=(traveltime bus stp hotel)15)
	        	(=(traveltime bus ldneye hotel)25)
	        	(=(traveltime bus hotel ldneye)25)
	        	(=(traveltime bus hotel stp)15)
	        	(=(traveltime bus trafalgsq hotel)20)
	        	(=(traveltime bus hotel trafalgsq)20)
	        	(=(traveltime bus trafalgsq stp)20)
	        	(=(traveltime bus stp trafalgsq)20)
	        	(=(traveltime bus trafalgsq ldneye)20)
	        	(=(traveltime bus ldneye trafalgsq)20)
				(=(traveltime walk stp ldneye)30)
	        	(=(traveltime walk ldneye stp)30)
	        	(=(traveltime walk stp hotel)5)
	        	(=(traveltime walk ldneye hotel)40)
	        	(=(traveltime walk hotel ldneye)40)
	        	(=(traveltime walk hotel stp)5)
	        	(=(traveltime walk trafalgsq hotel)35)
	        	(=(traveltime walk hotel trafalgsq)35)
	        	(=(traveltime walk trafalgsq stp)30)
	        	(=(traveltime walk stp trafalgsq)30)
	        	(=(traveltime walk trafalgsq ldneye)35)
	        	(=(traveltime walk ldneye trafalgsq)35)

                (=(visitfor ldneye tourist1)30)
	        	(=(visitfor stp tourist1)30)
                (=(visitfor trafalgsq tourist1)20))
	;;;;;;;;;;;; Problem GOALS ;;;;;;;;;;;;
	(:goal 
		(and 
			(at tourist1 hotel)
			(preference VisitStp (visited tourist1 stp))
			(preference VisitLdneye (visited tourist1 ldneye))
			(preference VisitTrafalgsq (visited tourist1 trafalgsq)))
	)
	;;;;;;;;;;;; Problem CONSTRAINTS ;;;;;;;;;;;;
	(:constraints 
	;; could use always, sometime, at-most-once, at end
		(and 
			(preference VisitStp (at end (visited tourist1 stp))) 
			(preference VisitLdneye (at end (visited tourist1 ldneye))) 
			(preference VisitTrafalgsq (at end (visited tourist1 trafalgsq)))
		)
	)
	;;;;;;;;;;;; Problem METRICS ;;;;;;;;;;;;
	(:metric minimize 
		(+ 
			(total-time) 
			(* 1000 
			; TBD:Total time weights 1000 more than violating VisitStp VisitLDneye and so on
			; the + sign indicates according to pddl http://www.cs.yale.edu/homes/dvm/papers/pddl-ipc5.pdf
			; that more than one parameter is accepted?
			; then a plan π that satisfy preference total time weights more than a plan 
			; that satisfies visiting all the places!
				(+ 	(is-violated VisitStp) 
					(is-violated VisitLdneye) 
					(is-violated VisitTrafalgsq)
				)
			)
		)
	)
)