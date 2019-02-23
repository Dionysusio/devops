import request from '@/utils/request'

// 获取书籍列表
export function getBooksList(params) {
  return request({
    url: '/api/book/',
    method: 'get',
    params
  })
}

// 更新图书信息
export function updateBooks(id, data) {
  return request({
    url: `/api/book/${id}/`,
    method: 'put',
    data
  })
}

// 删除图书
export function deleteBooks(id) {
  return request({
    url: `/api/book/${id}/`,
    method: 'delete'
  })
}

// 添加图书
export function createBooks(data) {
  return request({
    url: '/api/book/',
    method: 'post',
    data
  })
}
