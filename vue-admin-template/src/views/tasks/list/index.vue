<template>
  <div>
    <!--子组件表格-->
    <TasksList :value="autotasks"
               @edit="handleEdit"
               @detail="handleDetail" />
    <!--模态框-->
    <el-dialog :visible.sync="dialogVisibleForTask"
               title="任务详情"
               width="70%">
      <div>
        <pre>{{ exce_result }}</pre>
        <!--  pre: 默认数据长啥样,前端就显示啥样 -->
      </div>
    </el-dialog>
    <el-row type="flex"
            justify="center"
            style="padding-top:20px;">
      <span class="demonstration" />
      <el-pagination :total="total"
                     layout="prev, pager, next"
                     background
                     @current-change="handleChange" />
    </el-row>
  </div>
</template>
<script>
import { autotaskList, updateautotask, detailautotask } from '@/api/tasks/tasks'
import TasksList from './table'
export default {
  name: 'Tasks',
  components: {
    TasksList
  },
  data () {
    return {
      autotasks: [],
      total: 0,
      dialogVisibleForTask: false,
      exce_result: {},
      params: {
        page: 1
      }
    }
  },
  created () {
    this.fetchautotasklist()
  },
  methods: {
    fetchautotasklist () {
      autotaskList(this.params).then(res => {
        this.autotasks = res.results
        this.total = res.count
      })
    },
    handleEdit (value) { // 父组件执行任务
      const data = { 'status': 'Y' } // 执行完之后将状态改为Y
      updateautotask(value.id, data).then(res => {
        this.$message({
          message: '执行成功',
          type: 'success'
        })
        this.fetchautotasklist()
      })
    },
    handleDetail (id) {
      this.dialogVisibleForTask = true // 模态窗起来
      detailautotask(id).then(res => { // 拿到详情id
        console.log(res)
        this.exce_result = res.detail_result // 直接将res中的detail_result赋值给this.exce_result
      })
    },
    handleChange (val) {
      this.params.page = val
      this.fetchautotasklist()
    }
  }
}
</script>
<style lang="scss" scoped>
.task {
  padding: 10px;
}
pre {
  font-weight: bold;
  color: white;
  font-size: 16px;
  background-color: black;
}
</style>
