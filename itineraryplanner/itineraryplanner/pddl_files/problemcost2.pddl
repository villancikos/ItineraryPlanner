(define (problem test-tourist)
	(:domain touristinfo)
	(:objects stp hotel - location tourist1 - tourist bus walk - mode)
	(:init 	(open stp)
	        	(at tourist1 hotel)
	        	(path hotel stp)
	        	(path stp hotel)

	        	(=(traveltime bus stp hotel)15)	    
	        	(=(traveltime bus hotel stp)15)

	        	(=(traveltime walk stp hotel)5)
	        	(=(traveltime walk hotel stp)5)
	   
		(=(time-at stp)0)      
	     
	        	(=(visitfor stp tourist1)60))
                    
	(:goal (and (at tourist1 hotel)
		(preference TimeAtStp (>= (time-at stp) 60))
		(preference VisitStp (visited tourist1 stp))))
	(:constraints (and (preference TimeAtStp (at end (>= (time-at stp) 60)))(preference VisitStp (at end (visited tourist1 stp)))))
	(:metric minimize (- (* 1000 (is-violated VisitStp))(* 0.1 (time-at stp)))))