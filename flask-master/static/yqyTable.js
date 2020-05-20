;layui.use('table', function(){
  var table = layui.table;
  table.render({
    elem: '#sysVolTable',
    page:  {limit:1},//指定分页
    data: [{
    "srcIp": "192.168.0.1",
    "srcSys": "SRC",
    "destIp": "192.168.0.8",
    "destSys": "DEST",
    "startTime": "2017-12-25 9:31",
    "endTime": "2017-12-25 9:31",
    "remark":"yqy测试数据"
},{
    "srcIp": "192.168.0.1",
    "srcSys": "SRC",
    "destIp": "192.168.0.7",
    "destSys": "DEST",
    "startTime": "2017-12-27 18:31",
    "endTime": "2017-12-27 18:31",
    "remark":"yqy测试数据"
}],
    cols: [[
          {title:'序号',templet:'#indexTp1', width:'6%'},
          {field:'srcIp', title:'IP', width:'17%',sort:true},
          {field:'srcSys', title:'源系统', width:'10%'},
          {field:'destIp', title:'目标IP', width:'17%'},
          {field:'destSys', title:'目标系统', width:'10%'},
          {field:'startTime', title:'开始时间', width:'11%'},
          {field:'endTime', title:'结束时间', width:'11%'},
          {field:'remark', title:'备注'}
        ]]
  });
});