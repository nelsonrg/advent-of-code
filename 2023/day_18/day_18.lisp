(ql:quickload "cl-ppcre")

(defpackage :aoc-2023-18
  (:use :common-lisp)
  (:import-from :uiop :read-file-lines)
  (:import-from :cl-ppcre :register-groups-bind))
(in-package :aoc-2023-18)

(defun without-last (x)
  (reverse (rest (reverse x))))

(defun parse-line (x)
  "Parses the input"
  (register-groups-bind (a (#'parse-integer b) c) ("(\\w+) (\\d+) \\(\\#(\\w+)" x)
    (list (cons 'direction (char  a 0)) (cons 'distance b) (cons 'color c))))

(defun number->direction (x)
  "Converts number to direction"
  (case x
    (0 #\R)
    (1 #\D)
    (2 #\L)
    (3 #\U)))

(defun color->direction (x)
  "Converts color to distance and direction"
  (list (cons 'distance (parse-integer (subseq x 0 (- (length x) 1)) :radix 16))
	(cons 'direction (number->direction (parse-integer  (string (char x (-  (length x) 1))))))))

(defun direction->value (direction)
  "Converts direction character to alists"
  (case direction
    (#\R (list (cons 'dx 1) (cons 'dy 0)))
    (#\L (list (cons 'dx -1) (cons 'dy 0)))
    (#\D (list (cons 'dx 0) (cons 'dy 1)))
    (#\U (list (cons 'dx 0) (cons 'dy -1)))))

(defun next-vertex (start data)
  "Determines the next vertex based on the previous vertex and
distance/direction data"
  (let* ((x (rest (assoc 'x start)))
	 (y (rest (assoc 'y start)))
	 (direction (direction->value (rest (assoc 'direction data))))
	 (distance (rest (assoc 'distance data)))
	 (dx (rest (assoc 'dx direction)))
	 (dy (rest (assoc 'dy direction))))
    (list (cons 'x (+ x (* dx distance)))
	  (cons 'y (+ y (* dy distance))))))

(defun data->vertices (data start)
  "Converts distance and direction data to vertices"
  (let ((v (loop for d in data
		 with data = data
		 with start = start
		 do (setf start (next-vertex start d))
		 collect start)))
    (push start v)))

(defun shoelace (vertices)
  (let ((x (mapcar #'(lambda (a) (rest (assoc 'x a))) vertices))
	(y (mapcar #'(lambda (a) (rest (assoc 'y a))) vertices)))
    (floor (abs (- (reduce #'+ (mapcar #'* (without-last x) (rest y)))
		   (reduce #'+ (mapcar #'* (rest x) (without-last y)))))
	   2)))

(defun perimeter (data)
  (reduce #'+ (mapcar #'(lambda (x) (rest (assoc 'distance x))) data)))

(defun calculate-area (data start)
  (+ (shoelace (data->vertices data start))
     (/ (perimeter data) 2)
     1))

(defun part-1 (fname)
  "Run Day 18 part 1"
  (calculate-area (mapcar #'parse-line (read-file-lines fname))
		  (list (cons 'x 0) (cons 'y 0))))

(defun part-2 (fname)
  "Run Day 18 part 2"
  (calculate-area
   (mapcar
    #'(lambda (x) (color->direction (rest (assoc 'color x))))
    (mapcar #'parse-line (read-file-lines fname)))
   (list (cons 'x 0) (cons 'y 0))))

(defun main ()
  (format t "Part 1 test: ~D~%" (part-1 "test.txt"))
  (format t "Part 1: ~D~%" (part-1 "input.txt"))
  (format t "Part 2 test: ~D~%" (part-2 "test.txt"))
  (format t "Part 2: ~D~%" (part-2 "input.txt")))

(main)
