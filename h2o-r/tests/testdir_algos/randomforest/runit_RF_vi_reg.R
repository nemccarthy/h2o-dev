setwd(normalizePath(dirname(R.utils::commandArgs(asValues=TRUE)$"f")))
source('../../h2o-runit.R')


rfReg.vi.test<-
function(conn) {

    data2.hex <- h2o.uploadFile(conn, locate("smalldata/gbm_test/BostonHousing.csv"),
        key="data2.hex")
    x=1:13
    y=14
    rf <- h2o.randomForest(x, y, data2.hex, ntrees=100, max_depth=20,
                           min_rows=100)
    vi=match(rf@model$variable_importances[,1], colnames(data2.hex))

    expect_equal(vi[1:2], c(13,6))
    testEnd()
}
doTest("Variable Importance RF Test: Boston Housing Smalldata", rfReg.vi.test)
