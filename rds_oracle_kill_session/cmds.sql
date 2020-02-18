DECLARE
 CURSOR v_curqu IS
 SELECT SID, SERIAL#, USERNAME
 FROM V$SESSION WHERE USERNAME = 'CONSINCOMONITOR';
BEGIN
FOR rec in v_curqu
LOOP
rdsadmin.rdsadmin_util.kill(
        sid    => rec.Sid, 
        serial => rec.Serial#,
        method => 'IMMEDIATE');
END LOOP;
END;

set role dba;
alter user sfa default role connect, dba;

SELECT SID, SERIAL#, USERNAME
 FROM V$SESSION WHERE USERNAME = 'CONSINCOMONITOR';
 
begin
rdsadmin.rdsadmin_util.kill(
sid => 19,
serial => 4359,
method => 'IMMEDIATE');
end;

SELECT s.inst_id,
       s.sid,
       s.serial#,
       p.spid,
       S.Username,
       S.Program,
       'exec rdsadmin.rdsadmin_util.kill('||s.sid||','||s.serial#||');' as Execute_command
FROM   gv$session s
       Join Gv$process P On P.Addr = S.Paddr And P.Inst_Id = S.Inst_Id
Where  S.Type != 'BACKGROUND'
  AND s.username = UPPER('CONSINCOMONITOR');
