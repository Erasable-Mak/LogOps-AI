from core.anomaly_iforest import IFServiceModel
import numpy as np, scipy.sparse as sp
def test_iforest_smoke():
    X = sp.csr_matrix(np.random.randn(100, 20))
    m = IFServiceModel().fit(X)
    s = m.score(X)
    assert s.shape[0]==100
