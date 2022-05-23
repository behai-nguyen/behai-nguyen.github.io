select 
 de.dept_no,
 dep.dept_name,
 emp.*,
 de.from_date, 
 de.to_date
from
 (
	( select * from dept_emp where dept_no = 'd001' limit 100 ) union all 
	( select * from dept_emp where dept_no = 'd002' limit 100 ) union all 
	( select * from dept_emp where dept_no = 'd003' limit 100 ) union all 
	( select * from dept_emp where dept_no = 'd004' limit 100 ) union all 
	( select * from dept_emp where dept_no = 'd005' limit 100 ) union all 
	( select * from dept_emp where dept_no = 'd006' limit 100 ) union all 
	( select * from dept_emp where dept_no = 'd007' limit 100 ) union all 
	( select * from dept_emp where dept_no = 'd008' limit 100 ) union all 
	( select * from dept_emp where dept_no = 'd009' limit 100 )
 ) de
join departments dep on ( dep.dept_no = de.dept_no )
join employees emp on ( emp.emp_no = de.emp_no )
order by
dep.dept_name
;