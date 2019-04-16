<template>
  <div class="release">
    <div>
      <!--搜索-->
      <el-col :span="8">
        <el-input v-model="params.search"
                  placeholder="搜索"
                  @keyup.enter.native="searchClick">
          <el-button slot="append"
                     icon="el-icon-search"
                     @click="searchClick" />
        </el-input>
      </el-col>
    </div>

    <!--表格-->
    <deploy-list :value="release"
                 @edit="handleEdit" />

    <!--模态窗-->
    <el-dialog :visible.sync="dialogVisibleForEdit"
               title="发布详情"
               width="50%">
      <pre>{{ currentValue.console_output }}</pre>
    </el-dialog>

    <!--分页-->
    <center>
      <el-pagination :page-size="pagesize"
                     :total="totalNum"
                     background
                     layout="total, prev, pager, next, jumper"
                     @current-change="handleCurrentChange" />
    </center>
  </div>
</template>

<script>
import { getDeployList } from '@/api/release/release'
import DeployList from './table'

export default {
  name: 'Release',
  components: {
    DeployList
  },

  data () {
    return {
      dialogVisibleForEdit: false,
      currentValue: {},
      release: [],
      totalNum: 0,
      pagesize: 10,
      params: {
        page: 1,
        search: '',
        ordering: '-deploy_time',
        status: 3
      }
    }
  },

  created () {
    this.fetchData()
  },

  methods: {
    fetchData () {
      getDeployList(this.params).then(
        res => {
          this.release = res.results
          // console.log(this.release)
          this.totalNum = res.count
        })
    },
    handleCurrentChange (val) {
      this.params.page = val
      this.fetchData()
    },
    searchClick () {
      this.fetchData()
    },

    /* 查看发布结果，弹出模态窗 */
    handleEdit (value) {
      this.currentValue = { ...value }
      this.dialogVisibleForEdit = true
    }

  }

}
</script>

<style lang='scss' scoped>
pre {
  font-weight: bold;
  color: white;
  font-size: 16px;
  background-color: black;
}
</style>

