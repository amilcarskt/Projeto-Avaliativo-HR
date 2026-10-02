-- ============================================================================
-- Query 1: Salario por Departamento e Cargo
-- Disciplina: Visualizacao de Dados e Business Intelligence [T3]
-- Autor: Amilcar
-- Data: 01/10/2026
-- Banco: FreeSQL - Esquema HR (Human Resources)
--
-- Objetivo: Analisar a distribuicao de salarios por departamento e cargo.
-- Relacionamento: HR.EMPLOYEES com LEFT JOIN em HR.DEPARTMENTS e HR.JOBS
-- Filtro: Exclui funcionarios sem departamento alocado (DEPARTMENT_ID IS NOT NULL)
-- Resultado: 106 colaboradores com departamento e cargo identificados
-- ============================================================================

SELECT 
    e.EMPLOYEE_ID AS ID_FUNCIONARIO,
    e.FIRST_NAME || ' ' || e.LAST_NAME AS NOME_FUNCIONARIO,
    e.SALARY AS SALARIO,
    d.DEPARTMENT_NAME AS NOME_DEPARTAMENTO,
    j.JOB_TITLE AS TITULO_CARGO
FROM 
    HR.EMPLOYEES e
-- JOIN com DEPARTMENTS para obter o nome do departamento
LEFT JOIN 
    HR.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
-- JOIN com JOBS para obter o titulo e faixa salarial do cargo
LEFT JOIN 
    HR.JOBS j ON e.JOB_ID = j.JOB_ID
-- Remove o unico funcionario sem departamento alocado (ID 178 - Kimberely Grant)
WHERE 
    e.DEPARTMENT_ID IS NOT NULL
ORDER BY 
    d.DEPARTMENT_NAME ASC, e.SALARY DESC;