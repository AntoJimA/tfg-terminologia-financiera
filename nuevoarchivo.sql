USE ODECO;
SELECT *
FROM edp_datasets_odecoUpdKTrans
WHERE theme= 'Economy and finance';
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'edp_datasets_odecoUpdKTrans';

SELECT *
FROM edp_datasets_odecoUpdKTrans
WHERE dsLanguage = 'en'
  AND theme = 'Economy and finance';

  SELECT 
    id,
    title,
    COALESCE(description_eng, description) AS text_en,
    theme,
    keywords,
    hybrid_keywords
FROM edp_datasets_odecoUpdKTrans
WHERE dsLanguage = 'en'
  AND theme = 'Economy and finance';

  USE ODECO;

USE ODECO;

SELECT 
    id,
    COALESCE(description_eng, description) AS text_en,
    keywords_trans                        AS gold_keywords,
    theme,
    dsLanguage
FROM edp_datasets_odecoUpdKTrans
WHERE dsLanguage = 'en'
  AND theme = 'Economy and finance';

  USE ODECO;
GO

SELECT COUNT(*) AS total_filas
FROM edp_datasets_odecoUpdKTrans;
GO

USE ODECO;
GO

SELECT DISTINCT dsLanguage
FROM edp_datasets_odecoUpdKTrans
ORDER BY dsLanguage;
GO

SELECT DISTINCT langDetect
FROM edp_datasets_odecoUpdKTrans
ORDER BY langDetect;
GO

SELECT 
    id,
    COALESCE(description_eng, description) AS text_en,
    keywords_trans AS gold_keywords,
    theme,
    langDetect
FROM edp_datasets_odecoUpdKTrans
WHERE 
    langDetect = 'en'
    AND theme = 'Economy and finance';
GO