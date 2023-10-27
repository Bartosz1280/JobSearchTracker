
CREATE TABLE MyJobApplications (
    ApplicationID INT PRIMARY KEY AUTO_INCREMENT,
    Position VARCHAR(255) NOT NULL,
    Company VARCHAR(255) NOT NULL,
    Link VARCHAR(255) NOT NULL UNIQUE,
    ApplicationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    TypeCompany VARCHAR(255) NOT NULL,
    ApplicationStatus INT NOT NULL,
    ResponseDate DATE,
    InterviewDate DATE,
    TaskDate DATE,
    TechnicalInterviewDate DATE,
    AcceptanceDate DATE,
    RejectionDate DATE,
    RejectionReason VARCHAR(255),
    Notes TEXT,
    Modified DATETIME ON UPDATE CURRENT_TIMESTAMP
)


CREATE TABLE TestTable (
    ApplicationID INT PRIMARY KEY AUTO_INCREMENT,
    Position VARCHAR(255) NOT NULL,
    Company VARCHAR(255) NOT NULL,
    Link VARCHAR(255) NOT NULL UNIQUE,
    ApplicationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    TypeCompany VARCHAR(255) NOT NULL,
    ApplicationStatus INT NOT NULL,
    ResponseDate DATE,
    InterviewDate DATE,
    TaskDate DATE,
    TechnicalInterviewDate DATE,
    AcceptanceDate DATE,
    RejectionDate DATE,
    RejectionReason VARCHAR(255),
    Notes TEXT,
    Modified DATETIME ON UPDATE CURRENT_TIMESTAMP
)
;

CREATE TABLE ApplicationStatus (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Status VARCHAR(50) UNIQUE
);

INSERT INTO ApplicationStatus (Status)
VALUES 
        ('Applications submitted'),
        ('Replied'),
        ('Rejected before interview'),
        ('No reply'),
        ('Initial interviews'),
        ('Replied Too Late'),
        ('Task required/Technical interview scheduled'),
        ('No task/technical interview required'),
        ('Rejected by me'),
        ('Rejected after the first interview'),
        ('Final interview'),
        ('No additional interview'),
        ('Offer Received'),
        ('Rejected Before Offer'),
        ('Accepted'),
        ('Rejected');
