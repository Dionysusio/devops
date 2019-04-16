import request from '@/utils/request'

// 获取当前用户任务列表
export function getProjectList () {
  return request({
    url: '/list/',
    method: 'get'
  })
}

// 获取当前项目tag列表
export function getProjectTag (params) {
  return request({
    url: '/tag/',
    method: 'get',
    params
  })
}
