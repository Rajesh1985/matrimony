USE [manamalai]
GO

INSERT INTO [dbo].[profiles]
           ([name]
           ,[birth_date]
           ,[birth_time]
           ,[height_cm]
           ,[complexion]
           ,[caste]
           ,[sub_caste]
           ,[mobile_number]
           ,[introducer_name]
           ,[introducer_mobile]
           ,[created_at]
           ,[updated_at]
           ,[is_active])
     VALUES
            ('Raj'
           ,'1990-05-14'
           ,'12:45:00'
           ,175
           ,'Wheatish'
           ,'Vanniyar1'
           ,'Chengai'
           ,'99447'
           ,'Uma Pathy'
           ,'1234545'
           ,GETDATE()
           ,GETDATE()
           ,1)
GO


