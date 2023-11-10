import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useSnackbar } from "notistack";

import Stack from "@mui/material/Stack";

import MainLayout from "../layouts/full/mainlayout";
import TradeTable from "./subcomp/TradeTable";
import isEmpty from "../validation/isEmpty";
import Spinner from "./common/Spinner";

import { getTradesFromDatabase } from "../actions/tradesActions";

export default function TradesTable() {
  const [tableData, setTableData] = useState([]);
  const dispatch = useDispatch();
  const { enqueueSnackbar } = useSnackbar();
  const userId = useSelector((store) => store.auth.user.public_id);
  useEffect(() => {
    dispatch(getTradesFromDatabase({ user: userId }, enqueueSnackbar));
  }, [userId, dispatch, enqueueSnackbar]);

  const trades = useSelector((store) => store.trades);
  useEffect(() => {
    if (!isEmpty(trades.trades)) setTableData(trades.trades);
  }, [trades]);

  return (
    <MainLayout title="Trades Table">
      <Stack width="100%" p={{ xs: 1, md: 2 }} spacing={3}>
        {trades.loading ? (
          <Stack height="calc(100vh - 135px)" justifyContent="center">
            <Spinner />
          </Stack>
        ) : (
          <TradeTable dataToDisplay={tableData} />
        )}

        {/* <Paper sx={{ mb: 1, mt: 1, p: 1 }}>
                  Showing 5/9 Trades $14,402.57(RETURN $)
                </Paper> */}
      </Stack>
    </MainLayout>
  );
}
