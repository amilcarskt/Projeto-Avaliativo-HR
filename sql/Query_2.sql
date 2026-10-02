-- ============================================================================
-- Query 2: Funcionarios por Regiao (com Localizacao)
-- Disciplina: Visualizacao de Dados e Business Intelligence [T3]
-- Autor: Amilcar
-- Data: 01/10/2026
-- Banco: FreeSQL - Esquema HR (Human Resources)
--
-- Objetivo: Analisar salarios e distribuicao geografica dos colaboradores.
-- Relacionamento: HR.EMPLOYEES encadeado com DEPARTMENTS > LOCATIONS > COUNTRIES > REGIONS
-- Filtro: Garante integridade da hierarquia geografica ate o nivel continental
-- Resultado: 106 colaboradores com localizacao completa (Cidade, Estado, Pais e Regiao)
-- ============================================================================

SELECT 
    e.EMPLOYEE_ID AS ID_FUNCIONARIO,
    e.FIRST_NAME || ' ' || e.LAST_NAME AS NOME_FUNCIONARIO,
    e.SALARY AS SALARIO,
    d.DEPARTMENT_NAME AS NOME_DEPARTAMENTO,
    l.CITY AS CIDADE,
    l.STATE_PROVINCE AS ESTADO,
    c.COUNTRY_NAME AS PAIS,
    r.REGION_NAME AS REGIAO
FROM 
    HR.EMPLOYEES e
-- JOIN com DEPARTMENTS para obter o nome do departamento e o LOCATION_ID
LEFT JOIN 
    HR.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
-- JOIN com LOCATIONS para obter cidade e estado do departamento
LEFT JOIN 
    HR.LOCATIONS l ON d.LOCATION_ID = l.LOCATION_ID
-- JOIN com COUNTRIES para obter o nome do pais
LEFT JOIN 
    HR.COUNTRIES c ON l.COUNTRY_ID = c.COUNTRY_ID
-- JOIN com REGIONS para obter o continente/regiao geografica
LEFT JOIN 
    HR.REGIONS r ON c.REGION_ID = r.REGION_ID
-- Garante que o registro tenha a hierarquia geografica completa ate o continente
WHERE 
    r.REGION_NAME IS NOT NULL
ORDER BY 
    r.REGION_NAME ASC, e.SALARY DESC;