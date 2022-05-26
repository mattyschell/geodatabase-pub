declare @esriversion int
IF (EXISTS (SELECT * 
           FROM 
               INFORMATION_SCHEMA.TABLES 
           WHERE 
               TABLE_SCHEMA = 'dbo' 
           AND  TABLE_NAME = 'SDE_version'))
BEGIN 
    SELECT 
        major
    FROM
        dbo.SDE_version
END 