; Itinerary step from Queen's Theatre to Big Ben. Duration:1071;17.85
; Itinerary step from Queen's Theatre to Green Park. Duration:923;15.38
; Itinerary step from Queen's Theatre to McLaren London. Duration:1802;30.03
; Itinerary step from Big Ben to Queen's Theatre. Duration:1161;19.35
; Itinerary step from Big Ben to Green Park. Duration:972;16.2
; Itinerary step from Big Ben to McLaren London. Duration:2054;34.23
; Itinerary step from Green Park to Queen's Theatre. Duration:1001;16.68
; Itinerary step from Green Park to Big Ben. Duration:969;16.15
; Itinerary step from Green Park to McLaren London. Duration:1090;18.16
; Itinerary step from McLaren London to Queen's Theatre. Duration:1853;30.88
; Itinerary step from McLaren London to Big Ben. Duration:2034;33.9
; Itinerary step from McLaren London to Green Park. Duration:1040;17.33


(define (problem test-tourist)
	(:domain touristinfo)
	(:objects bigben greenpark mclarenlondon queens-theatre - location tourist1 - tourist walk - mode)
	(:init 
		;; Locations openning times.
		(at 600 (open queens-theatre))
		(at 1200 (not (open queens-theatre)))
		(at 600 (open bigben))
		(at 600 (open greenpark))
		(at 0 (open mclarenlondon))
		(at 1800 (not (open mclarenlondon)))
		;; Tourist Location
		(at tourist1 bigben	)

		;; Initializing paths?
		;; from queens-theatre
		(path queens-theatre bigben)
		(path queens-theatre greenpark)
		(path queens-theatre mclarenlondon)
		;; from bigben
		(path bigben queens-theatre)
		(path bigben greenpark)
		(path bigben mclarenlondon)
		;; from greenpark
		(path greenpark queens-theatre)
		(path greenpark bigben)
		(path greenpark mclarenlondon)
		;; from mclarenlondon
		(path mclarenlondon queens-theatre)
		(path mclarenlondon bigben)
		(path mclarenlondon greenpark)

		;; Travel Times Origin->Destination
		(=(traveltime walk queens-theatre bigben)17.85)
		(=(traveltime walk queens-theatre greenpark)15.38)		
		(=(traveltime walk queens-theatre mclarenlondon)30.03)
		(=(traveltime walk bigben queens-theatre)19.35)
		(=(traveltime walk bigben greenpark)16.2)
		(=(traveltime walk bigben mclarenlondon)34.23)
		(=(traveltime walk greenpark queens-theatre)16.68)
		(=(traveltime walk greenpark bigben)16.15)
		(=(traveltime walk greenpark mclarenlondon)18.16)	
		(=(traveltime walk mclarenlondon queens-theatre)30.88)
		(=(traveltime walk mclarenlondon bigben)33.9)
		(=(traveltime walk mclarenlondon greenpark)17.33)
				
        
		;; Duration of the visit at each place
        (=(visitfor queens-theatre tourist1)30)
        (=(visitfor bigben tourist1)30)
        (=(visitfor greenpark tourist1)30)
        (=(visitfor mclarenlondon tourist1)30))
		
		
	(:goal 
		(and 
			(at tourist1 bigben	)
			(preference Visitqueens-theatre (visited tourist1 queens-theatre))
			(preference VisitBigBen (visited tourist1 bigben))
			(preference VisitGreenPark (visited tourist1 greenpark))
			(preference VisitMclarenLondon (visited tourist1 mclarenlondon))
		)
	)

	(:constraints 
		(and 
			(preference Visitqueens-theatre (at end (visited tourist1 queens-theatre)))
			(preference VisitBigBen (at end (visited tourist1 bigben)))
			(preference VisitGreenPark (at end (visited tourist1 greenpark)))
			(preference VisitMclarenLondon (at end (visited tourist1 mclarenlondon)))
		)
	)
	;;PREGUNTA QUE PASA SI NO PONEMOS ESTO? COMO PODEMOS AFECTARLO?
	;;TODO DEPENDE DE SI PODEMOS IGNORAR EL ISVIOLATED?
	;;LA DUDA ES SI EN LAS PEFERENCIAS PONGO ESTO O QUE
	(:metric minimize 
		(+ 
			(total-time) 
			(* 1000 
				(+ 
					(is-violated Visitqueens-theatre) 
					(is-violated VisitBigBen) 
					(is-violated VisitGreenPark)
					(is-violated VisitMclarenLondon)
				)
			)
		)
	)
) ; program closing