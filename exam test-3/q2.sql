-- Design SQL tables for Students, Subjects, and Registrations with sample data and queries for multi-subject students and student count per subject.

CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    age INT
);

CREATE TABLE Subjects (
    subject_id INT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL
);

CREATE TABLE Registrations (
    registration_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);

INSERT INTO Students (student_id, student_name, age) VALUES
(1, 'Alice', 20),
(2, 'Bob', 21),
(3, 'Charlie', 22),
(4, 'Diana', 20),
(5, 'Ethan', 23);

INSERT INTO Subjects (subject_id, subject_name) VALUES
(101, 'Mathematics'),
(102, 'Physics'),
(103, 'Chemistry'),
(104, 'Computer Science'),
(105, 'English');

INSERT INTO Registrations (registration_id, student_id, subject_id) VALUES
(1, 1, 101),
(2, 1, 104),
(3, 2, 102),
(4, 2, 103),
(5, 3, 101),
(6, 4, 105),
(7, 5, 104),
(8, 5, 102);

SELECT s.student_id, s.student_name, COUNT(r.subject_id) AS subject_count
FROM Students s
JOIN Registrations r ON s.student_id = r.student_id
GROUP BY s.student_id, s.student_name
HAVING COUNT(r.subject_id) > 1;

SELECT sub.subject_id, sub.subject_name, COUNT(DISTINCT r.student_id) AS total_students
FROM Subjects sub
LEFT JOIN Registrations r ON sub.subject_id = r.subject_id
GROUP BY sub.subject_id, sub.subject_name;
