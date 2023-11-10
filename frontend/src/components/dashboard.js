import React from "react";
import Chart from "react-apexcharts";

import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";

import { useTheme } from "@mui/material/styles";

import MainLayout from "../layouts/full/mainlayout";

export default function Dashboard() {
  const optionscolumnchart = {
    chart: {
      type: "area",
      fontFamily: "'Plus Jakarta Sans', sans-serif;",
      foreColor: "#adb0bb",
      toolbar: {
        show: false,
      },
      height: 60,
      sparkline: {
        enabled: true,
      },
      group: "sparklines",
    },
    stroke: {
      curve: "smooth",
      width: 2,
    },
    fill: {
      colors: "blue",
      type: "solid",
      opacity: 0.05,
    },
    markers: {
      size: 0,
    },
    tooltip: {
      theme: "light",
    },
  };
  const seriescolumnchart = [
    {
      name: "",
      color: "#0094b6",
      data: [25, 66, 20, 40, 12, 58, 20],
    },
  ];

  // chart color
  const theme = useTheme();
  const primary = "#0094b6";
  const primarylight = "#ecf2ff";
  // const successlight = theme.palette.success.light;

  // donut chart
  const optionsdonutchart = {
    chart: {
      type: "donut",
      fontFamily: "'Plus Jakarta Sans', sans-serif;",
      foreColor: "#adb0bb",
      toolbar: {
        show: false,
      },
      height: 155,
    },
    colors: [primary, primarylight, "#F9F9FD"],
    plotOptions: {
      pie: {
        startAngle: 0,
        endAngle: 360,
        donut: {
          size: "75%",
          background: "transparent",
        },
      },
    },
    tooltip: {
      theme: theme.palette.mode === "dark" ? "dark" : "light",
      fillSeriesColor: false,
    },
    stroke: {
      show: false,
    },
    dataLabels: {
      enabled: false,
    },
    legend: {
      show: false,
    },
    responsive: [
      {
        breakpoint: 991,
        options: {
          chart: {
            width: 120,
          },
        },
      },
    ],
  };
  const seriesdonutchart = [55.88, 44.12];

  // chart with axis
  const axisChartseries = [
    {
      name: "Series 1",
      color: "#0094b6",
      data: [0.1, 0.5, 0.2, 0.8, 1, 0.6],
    },
  ];
  const axisChartOption = {
    chart: {
      id: "basic-bar",
    },
    xaxis: {
      categories: [],
    },
  };

  return (
    <MainLayout title="Dashboard">
      <Grid container spacing={{ xs: 1, md: 2 }} p={{ xs: 1, md: 2 }}>
        <Grid item xs={12} sm={6} lg={3}>
          <Paper sx={{ padding: 1 }}>
            <Grid
              container
              direction="row"
              alignItems="center"
              justifyContent="space-around"
            >
              <Grid item xs={6}>
                <Typography variant="body2">Accumulative Return EUR</Typography>
                <Typography>EUR 14,402.57</Typography>
              </Grid>
              <Grid item xs={6}>
                <Chart
                  options={optionscolumnchart}
                  series={seriescolumnchart}
                  type="area"
                  height="60px"
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <Paper sx={{ padding: 1 }}>
            <Grid
              container
              direction="row"
              alignItems="center"
              justifyContent="space-around"
            >
              <Grid item xs={6}>
                <Typography variant="body2">Profit Factor</Typography>
                <Typography>1.43</Typography>
              </Grid>
              <Grid item xs={6}>
                <Chart
                  options={optionscolumnchart}
                  series={seriescolumnchart}
                  type="area"
                  height="60px"
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <Paper sx={{ padding: 1 }}>
            <Grid
              container
              direction="row"
              alignItems="center"
              justifyContent="space-around"
            >
              <Grid item xs={6}>
                <Typography variant="body2">Avg Return EUR</Typography>
                <Typography>EUR 46.61</Typography>
              </Grid>
              <Grid item xs={6}>
                <Chart
                  options={optionscolumnchart}
                  series={seriescolumnchart}
                  type="area"
                  height="60px"
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <Paper sx={{ padding: 1 }}>
            <Grid
              container
              direction="row"
              alignItems="center"
              justifyContent="space-around"
            >
              <Grid item xs={6}>
                <Typography variant="body2">Win %</Typography>
                <Typography>55.88%</Typography>
              </Grid>
              <Grid item xs={6}>
                <Chart
                  options={optionsdonutchart}
                  series={seriesdonutchart}
                  type="donut"
                  height="82px"
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item xs={6} md={3}>
          <Paper sx={{ p: { xs: 1, sm: 1.5, md: 1, lg: 2 } }}>
            <Typography variant="h5">
              <b>$0.00</b>
            </Typography>
            <Stack direction="row" alignItems="flex-end" spacing={1} mt={2}>
              <Typography color="#0094b6" variant="h6">
                PnL
              </Typography>
              <Typography color="dimgray">Total</Typography>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={6} md={3}>
          <Paper sx={{ p: { xs: 1, sm: 1.5, md: 1, lg: 2 } }}>
            <Typography variant="h5">
              <b>0%</b>
            </Typography>
            <Stack direction="row" alignItems="flex-end" spacing={1} mt={2}>
              <Typography color="#0094b6" variant="h6">
                PnL
              </Typography>
              <Typography color="dimgray">% Charge</Typography>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={6} md={3}>
          <Paper sx={{ p: { xs: 1, sm: 1.5, md: 1, lg: 2 } }}>
            <Typography variant="h5">
              <b>$0.00</b>
            </Typography>
            <Stack direction="row" alignItems="flex-end" spacing={1} mt={2}>
              <Typography color="#0094b6" variant="h6">
                PnL
              </Typography>
              <Typography color="dimgray">/Day</Typography>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={6} md={3}>
          <Paper sx={{ p: { xs: 1, sm: 1.5, md: 1, lg: 2 } }}>
            <Typography variant="h5">
              <b>0.00</b>
            </Typography>
            <Stack direction="row" alignItems="flex-end" spacing={1} mt={2}>
              <Typography color="#0094b6" variant="h6">
                Volume
              </Typography>
              <Typography color="dimgray">/Day</Typography>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 1.5, position: "relative" }}>
            <Typography my={1} variant="subtitle1">
              Total PnL
            </Typography>
            <IconButton sx={{ position: "absolute", top: 10, right: 10 }}>
              <MoreHorizIcon />
            </IconButton>
            <Divider sx={{ mx: -1.5, mb: 1 }} />
            <Chart
              options={axisChartOption}
              series={axisChartseries}
              type="line"
              height={350}
            />
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 1.5, position: "relative" }}>
            <Typography my={1} variant="subtitle1">
              Daily PnL
            </Typography>
            <IconButton sx={{ position: "absolute", top: 10, right: 10 }}>
              <MoreHorizIcon />
            </IconButton>
            <Divider sx={{ mx: -1.5, mb: 1 }} />
            <Chart
              options={axisChartOption}
              series={axisChartseries}
              type="line"
              height={350}
            />
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 1.5, position: "relative" }}>
            <Typography my={1} variant="subtitle1">
              Daily Volume
            </Typography>
            <IconButton sx={{ position: "absolute", top: 10, right: 10 }}>
              <MoreHorizIcon />
            </IconButton>
            <Divider sx={{ mx: -1.5, mb: 1 }} />
            <Chart
              options={axisChartOption}
              series={axisChartseries}
              type="line"
              height={350}
            />
          </Paper>
        </Grid>
        <Grid item xs={6} md={3}>
          <Paper sx={{ p: { xs: 1, sm: 1.5, md: 1, lg: 2 } }}>
            <Typography variant="h5">
              <b>0%</b>
            </Typography>
            <Stack direction="row" alignItems="flex-end" spacing={1} mt={2}>
              <Typography color="#0094b6" variant="h6">
                Win rate
              </Typography>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={6} md={3}>
          <Paper sx={{ p: { xs: 1, sm: 1.5, md: 1, lg: 2 } }}>
            <Typography variant="h5">
              <b>0%</b>
            </Typography>
            <Stack direction="row" alignItems="flex-end" spacing={1} mt={2}>
              <Typography color="#0094b6" variant="h6">
                Win rate
              </Typography>
              <Typography color="dimgray">% Charge</Typography>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={6} md={3}>
          <Paper sx={{ p: { xs: 1, sm: 1.5, md: 1, lg: 2 } }}>
            <Typography variant="h5">
              <b>0</b>
            </Typography>
            <Stack direction="row" alignItems="flex-end" spacing={1} mt={2}>
              <Typography color="#0094b6" variant="h6">
                Wins
              </Typography>
              <Typography color="dimgray">Total</Typography>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={6} md={3}>
          <Paper sx={{ p: { xs: 1, sm: 1.5, md: 1, lg: 2 } }}>
            <Typography variant="h5">
              <b>0</b>
            </Typography>
            <Stack direction="row" alignItems="flex-end" spacing={1} mt={2}>
              <Typography color="#0094b6" variant="h6">
                Losses
              </Typography>
              <Typography color="dimgray">Total</Typography>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 1.5, position: "relative" }}>
            <Typography my={1} variant="subtitle1">
              Total Win Rate
            </Typography>
            <IconButton sx={{ position: "absolute", top: 10, right: 10 }}>
              <MoreHorizIcon />
            </IconButton>
            <Divider sx={{ mx: -1.5, mb: 1 }} />
            <Chart
              options={axisChartOption}
              series={axisChartseries}
              type="line"
              height={350}
            />
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 1.5, position: "relative" }}>
            <Typography my={1} variant="subtitle1">
              Daily Win Rate
            </Typography>
            <IconButton sx={{ position: "absolute", top: 10, right: 10 }}>
              <MoreHorizIcon />
            </IconButton>
            <Divider sx={{ mx: -1.5, mb: 1 }} />
            <Chart
              options={axisChartOption}
              series={axisChartseries}
              type="line"
              height={350}
            />
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 1.5, position: "relative" }}>
            <Typography my={1} variant="subtitle1">
              Total Win/Loss Score
            </Typography>
            <IconButton sx={{ position: "absolute", top: 10, right: 10 }}>
              <MoreHorizIcon />
            </IconButton>
            <Divider sx={{ mx: -1.5, mb: 1 }} />
            <Chart
              options={axisChartOption}
              series={axisChartseries}
              type="line"
              height={350}
            />
          </Paper>
        </Grid>
      </Grid>
    </MainLayout>
  );
}
